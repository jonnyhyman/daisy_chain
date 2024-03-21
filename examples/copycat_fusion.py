'''

    🐈 Copy Cat copies whatever the metadata
        field says on the current TimelineItem
        (and its MediaPoolItem) to the Clipboard!

'''

from daisychain import resolve
from time import sleep

proj = (resolve
       .get_project_manager()
       .get_current_project())

copy_field = "Comments"
copy_intvl = 1.0

# while True:

timeline = proj.get_current_timeline()
item_clip = timeline.get_current_video_item()
item_in_pool = item_clip.get_media_pool_item()

print(item_in_pool)

item_comp = item_clip.get_fusion_comp_by_index("1")
print(item_comp)
print()

# if item_in_pool:
#
#     # get the clip property from the media pool item
#     value = item_in_pool.get_clip_property(copy_field)
#
#     if value != "":
#         print(f'Copied: `{value}`')



sleep(copy_intvl)

