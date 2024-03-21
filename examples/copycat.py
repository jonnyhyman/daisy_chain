'''

    🐈 Copy Cat copies whatever the metadata
        field says on the current TimelineItem
        (and its MediaPoolItem) to the Clipboard!

    Requires:
    `pip install pyperclip`

'''

from daisychain import resolve
from time import sleep
import pyperclip

proj = (resolve
       .get_project_manager()
       .get_current_project())

copy_field = "Comments"
copy_intvl = 1.0

while True:

    timeline = proj.get_current_timeline()
    item_clip = timeline.get_current_video_item()

    '''
    ISSUE

    the below will fail if item_clip is None...

    Traceback (most recent call last):
  File "/Users/jonnyhyman/Human Creative Dropbox/Jonny Hyman/Compute/daisy_chain/examples/copycat.py", line 27, in <module>
    item_in_pool = item_clip.get_media_pool_item()
  File "/Users/jonnyhyman/Human Creative Dropbox/Jonny Hyman/Compute/daisy_chain/python/daisychain/resolve.py", line 741, in get_media_pool_item
    media_pool_item = self.rpc("GetMediaPoolItem")
  File "/Users/jonnyhyman/Human Creative Dropbox/Jonny Hyman/Compute/daisy_chain/python/daisychain/remote.py", line 64, in rpc
    return rpc(self.root, impl, *args, **kwargs)
  File "/Users/jonnyhyman/Human Creative Dropbox/Jonny Hyman/Compute/daisy_chain/python/daisychain/remote.py", line 42, in rpc
    raise(RPCError(resp['error']))
daisychain.remote.RPCError: TypeError: invalid command type: {'root': None, 'impl': 'GetMediaPoolItem', 'args': [], 'kwgs': {}}

    '''

    item_in_pool = item_clip.get_media_pool_item()

    if item_in_pool is not None:

        # get the clip property from the media pool item
        value = item_in_pool.get_clip_property(copy_field)

        if value != "":
            pyperclip.copy(value)
            print(f'Copied: `{value}`')
    

    # TODO: pause mechanism (perhaps a TUI?)

    sleep(copy_intvl)

print('Canceled!')
