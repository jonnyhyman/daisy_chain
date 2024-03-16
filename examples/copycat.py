'''

    🐈 Copy Cat copies whatever the metadata
        field says on the current TimelineItem
        to the Clipboard!

    Requires:
    `pip install pyperclip`

'''

from daisychain import resolve
import pyperclip

proj = (resolve
       .get_project_manager()
       .get_current_project())

curr = proj.get_current_timeline()
item = curr.get_current_video_item()
pool = item.get_media_pool_item()
print('Timeline:', curr.get_name())

if pool:
    print(f'    metadata: {pool.get_clip_property("Comments")}')
