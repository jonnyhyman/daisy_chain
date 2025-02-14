"""

🐈 Copy Cat copies whatever the metadata
    field says on the current TimelineItem
    (and its MediaPoolItem) to the Clipboard!

This example is more conveniently used via the
daisychain included command line script 'copycat'

Requires:
`pip install pyperclip`

"""

from daisychain import get_resolve
from time import sleep
import pyperclip

resolve = get_resolve()
proj = resolve.get_project_manager().get_current_project()

copy_field = "Comments"
copy_intvl = 5.0

print("🐈 Copy Cat is watching!")

while True:
    timeline = proj.get_current_timeline()
    item_clip = timeline.get_current_video_item()

    if item_clip is not None:
        item_in_pool = item_clip.get_media_pool_item()

        if item_in_pool is not None:
            # get the clip property from the media pool item
            value = item_in_pool.get_clip_property(copy_field)

            if value != "":
                pyperclip.copy(value)
                print(f"🐈 MEOW `{value}`")

    sleep(copy_intvl)
