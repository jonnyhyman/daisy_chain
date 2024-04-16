"""

    🥡 Collect copies or moves all the source media
        within the current timeline or media pool bin
        into the project folder root, maintaining the
        bin hierarchies defined within the media pool

    Requires `pip install aioshutil` for async file ops

    ⚠️ CAUTION, if a __move__ fails, you may lose your media
"""

import asyncio
from daisychain import get_resolve
from daisychain.resolve import MediaPool, MediaPoolFolder, MediaPoolItem, Project

from pathlib import Path

import aioshutil
import shutil

from typing import List, Tuple, Union

# options: ["copy", "move"]
collect_command = "copy"

# options: ["current_bin", "current_timeline"]
collect_from = "current_bin"

# collect_into = Path("/Users/jonnyhyman/Movies/DaisyChain Test/")
collect_into = Path(
    "/Users/jonnyhyman/Dropbox/Dr Becky/Night Sky News/April 2024/B-ROLL/"
)

confirm = False

if collect_command == "move":
    user = input(
        "WARNING: If a `move` command fails, you can lose your media. "
        "Are you sure you want to continue [y/n] > "
    )

    if user.lower() == "y":
        confirm = True

else:
    confirm = True

Collection = dict[str, Tuple[MediaPoolItem, Path]]
BinsMirror = dict[str, Tuple]


def paths_for_items(items: List[MediaPoolItem]) -> Collection:
    """
    Get the filepaths for all MediaPoolItems in the list
    and remove them if they do not have filepaths
    """
    collection: Collection = {}

    for item in items:
        uuid = item.get_unique_id()
        path = item.get_clip_property("File Path")
        path = Path(str(path))
        if path.exists():
            collection[uuid] = (item, path)

    return collection


def media_in_timeline(proj: Project) -> Collection:
    """
    Find the MediaPoolItems in the current timeline
    and zip them together into:
        [(item: MediaPoolItem, path: Path)]
    """
    print("> Getting media in timeline")
    tline = proj.get_current_timeline()

    items: List[MediaPoolItem] = []
    for track_type in ["video", "audio"]:
        for t in range(1, tline.get_track_count(track_type) + 1):
            clips = tline.get_item_list_in_track(track_type, t)
            for clip in clips:
                item = clip.get_media_pool_item()
                if item:
                    items.append(item)

    return paths_for_items(items)


def media_in_bin(pool: MediaPool) -> Collection:
    """
    Find the MediaPoolItems in the current media bin
    (recursively into subbins) zip them together into:
        [(item: MediaPoolItem, path: Path)]
    """
    print("> Getting media in bin")
    root = pool.get_current_folder()

    def crawl(
        elem: Union[MediaPoolItem, MediaPoolFolder],
        curr: List[MediaPoolItem],
    ) -> List[MediaPoolItem]:
        if isinstance(elem, MediaPoolItem):
            curr.append(elem)
        else:
            # add clip item
            for clip in elem.get_clip_list():
                curr.append(clip)

            # recurse into subfolders
            for fold in elem.get_subfolder_list():
                crawl(fold, curr)

        return curr

    items = crawl(root, [])

    return paths_for_items(items)


def ensure_disk_space(collection: Collection):
    """
    Ensure enough disk space on hard drive to collect
    """
    # returns bytes, we'll compare in MB
    _, _, free = shutil.disk_usage(__file__)
    avail_MB = free * 1e-6
    total_MB = 0.0
    for _, (_, path) in collection.items():
        total_MB += (path.stat().st_size) * 1e-6
        if total_MB >= avail_MB:
            raise (
                OverflowError(
                    f"""FAILED: Not enough disk space! """
                    f"""Collect requires at least """
                    f"""{total_MB*1e-3:.2f} GB but """
                    f"""only {avail_MB*1e-3:.2f} GB on Disk"""
                )
            )


def discover_parents(pool: MediaPool, collection: Collection) -> BinsMirror:
    """
    Build a mirror of the media pool including only
    the items we have in the `collection`.
    """
    print("> Building media pool mirror")

    def crawl(
        elem: Union[MediaPoolItem, MediaPoolFolder],
        addr: Tuple,
        curr: BinsMirror,
        foci: Tuple[str, ...],
    ):
        """
        Recursive media pool crawler encoding
        a flat map of the path of each collect
        {
            # name    : location
            "A.mp4"   : ["Master"],
            'BinName' : ["Master", "A", "B"],
        }
        """
        uuid = elem.get_unique_id()
        name = elem.get_name()  # move to uuid later

        # print(f'... crawl @ {"/".join(addr)} > {name} {curr} ')

        if isinstance(elem, MediaPoolItem):
            if uuid in foci:
                curr[uuid] = tuple(addr)

        elif isinstance(elem, MediaPoolFolder):
            # basically `cd ./this_bin`
            new_addr = (*addr, name)

            # add clip item
            for clip in elem.get_clip_list():
                crawl(clip, new_addr, curr, foci)

            # recurse into subfolders
            for fold in elem.get_subfolder_list():
                crawl(fold, new_addr, curr, foci)

    # get only the items in the collection
    # so that mirror is 1:1 with collection
    foci = tuple(collection.keys())

    mirror: BinsMirror = {}
    crawl(pool.get_root_folder(), (), mirror, foci)

    return mirror


def new_src_dirs(mirror: BinsMirror):
    """Make directories in the project folder to match"""
    print("> Making mirror directories")

    new_src = {}
    for uuid, addr in mirror.items():
        if len(addr) > 1:
            path = collect_into.joinpath(*addr[1:])
            path.mkdir(parents=True, exist_ok=True)
            new_src[uuid] = path.resolve()

        else:
            # don't need to make folders
            # for the root items
            new_src[uuid] = collect_into.resolve()

    return new_src


async def transfer(
    collection: Collection,
    newsrc: dict[str, Path],
    move: bool = False,
):
    tasks = []

    for uuid, (_, path) in collection.items():
        src = path
        dst = newsrc[uuid] / path.name

        if src.is_dir:
            # timelines seen as dirs for whatever reason
            continue

        if move:
            print(f"> Move {src} to {dst}")
            tasks.append(aioshutil.move(src, dst))
        else:
            print(f"> Copy {src} to {dst}")
            tasks.append(aioshutil.copy(src, dst))

    await asyncio.gather(*tasks)


def relink(collection: Collection, newsrc: dict[str, Path]):
    print("> Relinking media items")
    for uuid, (item, path) in collection.items():
        repl = newsrc[uuid] / path.name
        item.replace_clip(str(repl.absolute()))


async def collect():
    """Collect runner"""

    resolve = get_resolve()

    proj = resolve.get_project_manager().get_current_project()
    pool = proj.get_media_pool()

    # detect collection of media in `collect_from`
    if collect_from == "current_bin":
        collection = media_in_bin(pool)
    elif collect_from == "current_timeline":
        collection = media_in_timeline(proj)
    else:
        raise (ValueError("{collect_from} not a valid option"))

    # get file sizes in collection to ensure free disk space
    ensure_disk_space(collection)

    # detect media bin & item hierarchies
    mirror = discover_parents(pool, collection)

    # rebuild media bin hierarchy on file system
    newsrc = new_src_dirs(mirror)

    # async copy or move all file paths on file system
    if collect_command == "move":
        await transfer(collection, newsrc, True)
    else:
        await transfer(collection, newsrc, False)

    # relink all media items in collection to new places
    relink(collection, newsrc)


asyncio.run(collect())
