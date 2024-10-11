from daisychain import get_resolve
from daisychain.resolve import MediaPool
from watchfiles import watch as filewatch
import click

# stdlib
from typing import Tuple
from pathlib import Path

resolve_importables = [
    ".mp3",
    ".wav",
    ".m4a",
    ".mov",
    ".mp4",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".png",
]


def watch_mode(mpool: MediaPool, thisdir: str = "./"):

    watch = Path(thisdir)
    print(f'👀 Watching {watch.absolute()}')

    for changes in filewatch(watch):
        for change in changes:
            change_type, path = change
            path = Path(path)

            if str(change_type) != "Change.added":
                continue

            print(f"> Importing {path} into project")
            mitems = mpool.import_media([str(path.resolve())])

            if not len(mitems): # Resolve's API fails silently...
                print(f"! Failed for unspecified reason: {path}")


@click.command()
@click.argument("filepaths", type=click.Path(exists=True), nargs=-1)
@click.option(
    "--watch",
    is_flag=True,
    default=False,
    help="Watch current directory for new files, importing when added",
)
def main(filepaths: Tuple[str, ...], watch: bool = False):
    """Processes the given file path and converts it to an absolute path."""

    resolve = get_resolve()
    mpool = resolve.get_project_manager().get_current_project().get_media_pool()

    if watch and len(filepaths) == 0:
        watch_mode(mpool)

    elif watch:
        watch_mode(mpool, filepaths[0])

    else:
        if len(filepaths) == 0:
            print("❓ No filepaths specified")
            return

        paths = [Path(p) for p in filepaths]
        paths = [str(p.absolute()) for p in paths if p.suffix in resolve_importables]
        clips = mpool.import_media(paths)

        if len(clips) == 0:
            print("❌ All media failed to import")

        if len(clips) != len(paths):
            print("💩 Some media failed to import")

        else:
            print("✅ Successfully imported all media")
