"""
# 🎞️ Auto Import

Ongoing script to import new files
from the target watch folder into
A) the currently open media bin
B) the media bin specified

Requires:
    `pip install watchfiles`
"""

from daisychain import get_resolve  # , resolve_importables
from watchfiles import watch
from pathlib import Path

resolve = get_resolve()

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

use_initial_bin = False
# ^ if True, will always import into the bin that current at script start
# ^ if False, will always import into current bin, no matter where it is
watch_dir = Path(
    # "/Users/jonnyhyman/Dropbox/Dr Becky/Night Sky News/April 2024/B-ROLL/SCREEN GRABS/"
    "C:/Users/jonny/Dropbox/Dr Becky/Night Sky News/April 2024/B-ROLL/SCREEN GRABS/"
)

print(f"> Listening for changes in {watch_dir}")

media_pool = resolve.get_project_manager().get_current_project().get_media_pool()
init_folder = media_pool.get_current_folder()

for changes in watch(watch_dir):
    for change in changes:
        change_type, path = change
        path = Path(path)

        if str(change_type) != "Change.added":
            continue

        if path.suffix in resolve_importables:
            if use_initial_bin:
                media_pool.set_current_folder(init_folder)

            print(f"> Importing {path} into project")
            mitems = media_pool.import_media([str(path.resolve())])

            if not len(mitems):
                print(f"! FAILED for unspecified reason: {path}")

        else:
            print("! FAILED: not importable into Resolve: {mfile}")
