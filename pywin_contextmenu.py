# coding=utf-8
# (c) Naveen Namani
# https://github.com/naveennamani
import os
import sys
import warnings
from enum import Enum
from winreg import CloseKey
from winreg import CreateKey
from winreg import DeleteKey
from winreg import EnumKey
from winreg import HKEYType
from winreg import HKEY_CLASSES_ROOT
from winreg import HKEY_CURRENT_USER
from winreg import OpenKey
from winreg import QueryInfoKey
from winreg import REG_SZ
from winreg import SetValue
from winreg import SetValueEx


################################################################################
# Enum classes for defining RootType and UserType
################################################################################
class RootType(str, Enum):
    DIR = r"Directory\\shell\\"
    DIR_BG = r"Directory\\Background\\shell\\"
    DESKTOP_BG = r"DesktopBackground\\shell\\"
    DRIVE = r"Drive\\shell\\"
    ALL_FILES = r"*\\shell\\"
    FILE = r"SystemFileAssociations\\{FILE_TYPE}\\shell\\"


class UserType(Enum):
    CURR_USER = HKEY_CURRENT_USER
    ROOT = HKEY_CLASSES_ROOT


################################################################################
# classes for storing the information about ContextMenuItem and ContextMenuGroup
################################################################################
class ContextMenuItem(object):
    def __init__(self, item_name, command, item_reg_key = "", icon = "",
                 extended = False):
        self.item_name = item_name
        self.item_reg_key = item_name if item_reg_key == "" else item_reg_key
        self.icon = icon
        self.command = command
        self.extended = extended


class ContextMenuGroup(object):
    def __init__(self, group_name, group_reg_key = "", icon = "",
                 extended = False):
        self.group_name = group_name
        self.group_reg_key = group_name if group_reg_key == "" else group_reg_key
        self.icon = icon
        self.items = []
        self.extended = extended

    def add_item(self, item):
        assert isinstance(
            item, (ContextMenuItem, ContextMenuGroup)
        ), "Please pass instance of ContextMenuItem or ContextMenuGroup"
        self.items.append(item)


################################################################################
# Custom Exceptions
################################################################################
class CyclicGroupException(Exception):
    pass


################################################################################
# Utility functions
################################################################################
def get_root(user_type: UserType, root_type: RootType,
             file_type: str = None) -> HKEYType:
    """
    Pass user_type and root_type and get a top level Registry key for creating
    context menus.
    :param user_type: Field of UserType enum
    :param root_type: Field of RootType enum
    :param file_type: FILE_TYPE to be used if the root_type is RootType.FILE
    :return: HKEYType registry key
    """
    if user_type is UserType.CURR_USER:
        root_type = r"Software\\Classes\\" + root_type.value
    else:
        root_type = root_type.value
    if "{FILE_TYPE}" in root_type:
        if file_type is None:
            raise ValueError(
                'Please provide a FILE_TYPE you want\n'
                'Usage example: get_root(user_type, RootType.FILE, r".zip")')
        else:
            root_type = root_type.format(FILE_TYPE = file_type)
    return CreateKey(user_type.value, root_type)


def python_script_cmd(
        script_path: str,
        rel_path: bool = False,
        hide_terminal: bool = False
) -> str:
    """
    Convert a python script path to an executable command
    :param script_path: path to the python script
    :param rel_path: if the given path is relative to the current directory
    :param hide_terminal: whether to hide the python terminal during executing
    """
    if rel_path:
        script_path = os.path.join(os.getcwd(), script_path)
    py_executable = sys.executable.replace(
        "python.exe", "pythonw.exe") if hide_terminal else sys.executable
    return f'{py_executable} "{script_path}" "%V"'


def is_cyclic_group(group: ContextMenuGroup, all_group_reg_keys = None) -> bool:
    if all_group_reg_keys is None:
        all_group_reg_keys = [group.group_reg_key]
    for item in group.items:
        if isinstance(item, ContextMenuGroup):
            if item.group_reg_key not in all_group_reg_keys:
                all_group_reg_keys.append(item.group_reg_key)
                if is_cyclic_group(item, all_group_reg_keys):
                    return True
            else:
                return True
    return False


def _del_key(rk):
    no_subkeys, _, __ = QueryInfoKey(rk)
    # print(no_subkeys)
    for i in range(no_subkeys):
        sk = EnumKey(rk, 0)
        # print(sk)
        _del_key(OpenKey(rk, sk))
    DeleteKey(rk, "")


################################################################################
# core functionality
################################################################################
def create_item(root_key, item: ContextMenuItem):
    item_key = CreateKey(root_key, item.item_reg_key)
    SetValue(item_key, "", REG_SZ, item.item_name)
    SetValue(item_key, "command", REG_SZ, item.command)
    if item.icon != "":
        SetValueEx(item_key, "Icon", 0, REG_SZ, item.icon)
    if item.extended:
        SetValueEx(item_key, "Extended", 0, REG_SZ, "")
    CloseKey(item_key)


def create_group(root_key, group: ContextMenuGroup):
    if is_cyclic_group(group):
        raise CyclicGroupException(
            "Congratulations! You're about to break your registry")
    group_key = CreateKey(root_key, group.group_reg_key)

    SetValueEx(group_key, "MUIVerb", 0, REG_SZ, group.group_name)
    SetValueEx(group_key, 'SubCommands', 0, REG_SZ, "")
    if group.icon != "":
        SetValueEx(group_key, "Icon", 0, REG_SZ, group.icon)
    if group.extended:
        SetValueEx(group_key, "Extended", 0, REG_SZ, "")

    subcommands_key = CreateKey(group_key, "shell")

    for item in group.items:
        if isinstance(item, ContextMenuItem):
            create_item(subcommands_key, item)
        elif isinstance(item, ContextMenuGroup):
            create_group(subcommands_key, item)
    CloseKey(subcommands_key)
    CloseKey(group_key)


def delete_item(root_key, item_reg_key):
    try:
        _del_key(OpenKey(root_key, item_reg_key))
    except FileNotFoundError:
        warnings.warn(
            "There is an error deleting the key, are you sure the key exists?")
    except:
        from traceback import print_exc
        print_exc()


if __name__ == '__main__':
    group1 = ContextMenuGroup("Group 1")
    group2 = ContextMenuGroup("Group 2")
    group3 = ContextMenuGroup("Group 3")

    group1.add_item(group2)
    group2.add_item(group3)

    group1.add_item(ContextMenuItem("Item 1", "cmd.exe"))
    group1.add_item(ContextMenuItem("Item 2", "cmd.exe"))

    group2.add_item(ContextMenuItem("Item 3", "cmd.exe"))
    group2.add_item(ContextMenuItem("Item 4", "cmd.exe"))

    group3.add_item(ContextMenuItem("Item 5", "cmd.exe"))
    group3.add_item(ContextMenuItem("Item 6", "cmd.exe"))

    user_root = get_root(UserType.CURR_USER, RootType.DIR_BG)
    create_group(user_root, group1)

    input("Group 1 created, press ENTER to continue")

    delete_item(user_root, "Group 1")
    CloseKey(user_root)

    input("Group 1 deleted, press ENTER to close")
