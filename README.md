# pywin_contextmenu

A simple and intuitive way to add your custom scripts to your windows right click contextmenu.

## Usage
```python
import pywin_contextmenu as pycm

# create a group
group1 = pycm.ContextMenuGroup("My python scripts")

# convert your script into executable command
script_cmd = pycm.python_script_cmd("scripts/clean_empty_folders.py", rel_path = True, hide_terminal = True)

# create the item
item1 = pycm.ContextMenuItem("Clean empty folders", script_cmd)

# add item to the group
group1.add_item(item1)

# get root_key
rk = pycm.get_root(pycm.UserType.CURR_USER, pycm.RootType.DIR_BG)

# Create the group and test
pycm.create_group(rk, group1)
```

## API
The script depends on two main classes `ContextMenuItem` and `ContextMenuGroup`.

### `ContextMenuItem`
This is the menu item which triggers and launches the command when clicked in the contextmenu.
The signature of this class is
```python
ContextMenuItem(
    item_name, # name of the item to be shown 
    command, # command to be executed when selected
    item_reg_key = "", # registry key associated with the item
                       # (if not given will be treated as item_name)
    icon = "" # path to an icon to be shown with the item
)
```
### `ContextMenuGroup`
This class groups multiple items and subgroups.
```python
ContextMenuGroup(
    group_name, # name of the group to be shown
    group_reg_key = "", # registry key associated with the group
    icon = "" # path to an icon to be shown with the group
)
```
For adding items or groups to a group instance call add_item method of the class.
```python
ContextMenuGroup.add_item(item)
# or
ContextMenuGroup.add_item(subgroup)
```

## Methods available

* `RootType` - an `Enum` for chosing where the context menu item/group will be displayed
* `UserType` - an `Enum` for chosing whether to add the context menu for current user or for all users
* `get_root(user_type: UserType, root_type: RootType, file_type: str)` - creates/opens the registry key for the selected user_type and root_type.
 If the `root_type` is `RootType.FILE` then `file_type` argument is required and indicates the file extention.
* `python_script_cmd(script_path, rel_path = False, hide_terminal = False)` - a utility function to convert a given `script_path` to an executable command.
* `create_item(root_key, item: ContextMenuItem)` - adds the `item` to the context menu
* `create_group(root_key, group: ContextMenuGroup)` - adds the `group` to the context menu
* `delete_item(root_key, item_reg_key)` - deletes the `item_reg_key` at the given `root_key` registry.
 **Warning:** Please ensure you're not deleting the keys at the top level registry keys (e.g. `HKEY_CLASSES_ROOT`, `HKEY_CURRENT_USER` etc.)
---
# &copy; Naveen Namani