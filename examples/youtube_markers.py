from daisychain import get_resolve
from datetime import timedelta
from pprint import pprint
import pyperclip 

resolve = get_resolve()
timeline = resolve.get_project_manager().get_current_project().get_current_timeline()
markers = timeline.get_markers()
framerate = timeline.get_setting("timelineFrameRate")

description = ""
for frame, marker in markers.items():
    seconds = int(frame)/framerate
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    timestamp = f"{int(minutes):02d}:{int(seconds):02d}"
    description += f"{timestamp} {marker['name']}\n"

pyperclip.copy(description)

print('Copied to clipboard\n------')
print(description)

