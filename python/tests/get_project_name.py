from daisychain import resolve

pmgr = resolve.get_project_manager()
print('pmgr', pmgr)

proj = pmgr.get_current_project()
print('proj', proj)

name = proj.get_name()
print('name', name)

# project_name = daisychain.get_project_manager().get_project().get_name()
# print(project_name)
