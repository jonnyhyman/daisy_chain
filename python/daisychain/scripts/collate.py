from typing import Callable

import click
from daisychain import get_resolve
from daisychain.resolve import MediaPoolFolder
from pathlib import Path
import shutil


def file_action(src_file: Path, dst_file: Path, action="copy"):
    src_file = src_file.absolute()
    dst_file = dst_file.absolute()

    print("...", src_file, dst_file)

    if src_file == dst_file:
        return

    if action == "copy":
        try:
            shutil.copyfile(src_file, dst_file)
        except shutil.SameFileError:
            pass  # already been moved
    elif action == "move":
        try:
            shutil.move(src_file, dst_file)
        except shutil.SameFileError:
            pass  # already been moved
    else:
        raise NotImplementedError


def walk_down(root: MediaPoolFolder, path: list[str], action: str):
    into_path = Path("/".join(path))
    into_path.mkdir(exist_ok=True)

    # Collect the clips in the folder
    for clip in root.get_clip_list():
        file_path = clip.get_clip_property("File Path")  # "clipPath" ???
        assert isinstance(file_path, str)
        file_path = Path(file_path)
        if file_path.exists() == False or file_path.is_file() == False:
            print("... Not a media file")
            continue
        else:
            print(f"... Is a media file: {file_path}")
        into_file = into_path / file_path.name
        print(
            f"Relink and {action}\n"
            f"    {clip.get_name()}\n"
            f"    {file_path}\n"
            f"    {file_path.absolute()}\n"
            f"    {into_file.absolute()}"
        )
        file_action(file_path, into_file, action)
        clip.replace_clip(str(into_file.absolute()))

    # Recurse into sub-folders
    for fold in root.get_subfolder_list():
        walk_down(fold, path + [fold.get_name()], action)


@click.command()
@click.option("-a", "--action", default="copy")
@click.option(
    "-d", "--dst", type=click.Path(exists=True, file_okay=False), default=Path("./")
)
def main(action: str, dst):
    resolve = get_resolve()
    media_pool = resolve.get_project_manager().get_current_project().get_media_pool()
    # TODO
    # implement a "timeline" focus, and allow subfolders for clips to be defined
    # by a timeline markers of a specified color that denote the start of a 'section'
    current_bin = media_pool.get_current_folder()
    walk_down(current_bin, [str(dst.absolute())], action)


main()
