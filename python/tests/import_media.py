from daisychain import get_resolve
from pathlib import Path

resolve = get_resolve()

pool = resolve.get_project_manager().get_current_project().get_media_pool()

print("pool ->", pool)

new = pool.import_media([Path("/Users/jonnyhyman/Movies/June.mov")])

print("added ->", [n.get_name() for n in new])
