![PyPI](https://img.shields.io/pypi/v/pywin_contextmenu)
![PyPI - Downloads](https://img.shields.io/pypi/dd/pywin_contextmenu)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/naveennamani/pywin_contextmenu)
![GitHub last commit](https://img.shields.io/github/last-commit/naveennamani/pywin_contextmenu)


# pywin_contextmenu

A simple and intuitive way to add your custom scripts to your windows right click contextmenu.

## Installation

You can download the pywin_contextmenu.py file from this repository (https://raw.githubusercontent.com/naveennamani/pywin_contextmenu/master/pywin_contextmenu.py) and place the file in your scripts folder.

Or you can install this package from pypi using
```shell script
pip install pywin_contextmenu
```
and simply import in your scripts.
```python
import pywin_contextmenu as pycm
```

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
# or
group1.add_items([item1])

# get root_key
rk = pycm.get_root(pycm.UserType.CURR_USER, pycm.RootType.DIR_BG)

# Create the group and test
group1.create(rk)

########################
# In a more pythonic way
########################
pycm.ContextMenuGroup("Group 1", items = [
    pycm.ContextMenuItem("Open CMD", "cmd.exe"),
    pycm.ContextMenuItem("Open CMD 2", "cmd.exe")
]).create(
    pycm.get_root(pycm.UserType.CURR_USER, pycm.RootTYpe.DIR_BG)
)
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
    icon = "", # path to an icon to be shown with the item
    extended = False # set to True if the item is to be shown when right clicked with shift button
)
```
For creating the item simply call the `.create` method.
```
ContextMenuItem.create(root_key) # Create the item at the given registry root_key
```
### `ContextMenuGroup`
This class groups multiple items and subgroups.
```python
ContextMenuGroup(
    group_name, # name of the group to be shown
    group_reg_key = "", # registry key associated with the group
    icon = "", # path to an icon to be shown with the group
    extended = False, # set to True if the group is to be shown when right clicked with shift button
    items = [] # items to be displayed on this group
)
```
For adding items or groups to a group instance call `add_item`/`add_items` method of the class.
```python
ContextMenuGroup.add_item(item)
# or
ContextMenuGroup.add_item(subgroup)
# for multiple items
ContextMenuGroup.add_items([item1, item2, subgroup1, subgroup2])
```
###### Note: The same functionality will be achieved if the items are passed during the creation of `ContextMenuGroup` object by passing the items using `items` keyword.
Then to create the group and add to the contextmenu simply call `.create` with the key obtained from `get_root` function as argument.
```
ContextMenuGroup.create(root_key) # Create the group and add to contextmenu
```

#### Note: All methods of `ContextMenuItem` and `ContextMenuGroup` returns `self`, so they can be chained. Adding items to `ContextMenuGroup` will not add them to the contextmenu/registry unless `.create` method is called.
## Utility methods available

* `RootType` - an `Enum` for chosing where the context menu item/group will be displayed
* `UserType` - an `Enum` for chosing whether to add the context menu for current user or for all users
* `get_root(user_type: UserType, root_type: RootType, file_type: str)` - creates/opens the registry key for the selected user_type and root_type.
 If the `root_type` is `RootType.FILE` then `file_type` argument is required and indicates the file extention.
* `python_script_cmd(script_path, rel_path = False, hide_terminal = False)` - a utility function to convert a given `script_path` to an executable command.
* `delete_item(root_key, item_reg_key)` - deletes the `item_reg_key` at the given `root_key` registry.
 **Warning:** Please ensure you're not deleting the keys at the top level registry keys (e.g. `HKEY_CLASSES_ROOT`, `HKEY_CURRENT_USER` etc.)

# TODO
* [ ] Add a way to handle passing of multiple files/folders to the selected script without launching multiple instances of the script.

---
# &copy; Naveen Namani