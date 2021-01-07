# coding=utf-8
# (c) Naveen Namani
# https://github.com/naveennamani/pywin_contextmenu
# __version__ = 2021.1.7
import os
import sys
import warnings
from enum import Enum
from inspect import isfunction
from pathlib import Path
from typing import Callable
from typing import List
from typing import Union
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

__version__ = (2021, 1, 7)


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
# Custom Exceptions
################################################################################
class CyclicGroupException(Exception):
    pass


################################################################################
# classes for storing the information about ContextMenuItem and ContextMenuGroup
################################################################################
class ContextMenuItem(object):
    def __init__(
            self,
            item_name: str,  # to be displayed in the contextmenu
            command: str,  # command to be executed
            item_reg_key: str = "",  # key to be used in the registry
            icon: str = "",  # path to the icon to be shown along with item
            extended: bool = False  # if true, item will be shown with shift key
    ):
        self.item_name = item_name
        self.item_reg_key = item_name if item_reg_key == "" else item_reg_key
        self.icon = icon
        self.command = command
        self.extended = extended

    def create(self, root_key: HKEYType):
        """
        Adds entries into the registry for creating the item
        :param root_key: HKEYType key where the item is to be created.
                         Obtain the key using `get_root` function
        :return: Returns the ContextMenuItem item
        """
        item_key = CreateKey(root_key, self.item_reg_key)
        SetValue(item_key, "", REG_SZ, self.item_name)
        SetValue(item_key, "command", REG_SZ, self.command)
        if self.icon != "":
            SetValueEx(item_key, "Icon", 0, REG_SZ, self.icon)
        if self.extended:
            SetValueEx(item_key, "Extended", 0, REG_SZ, "")
        CloseKey(item_key)
        return self

    def create_for(self, user_type: UserType, root_types: List[RootType]):
        """
        Add the item to multiple locations
        Usage: contextmenu_item.create_for(UserType.CURR_USER, [RootType.DIR, RootType.DIR_BG])
        """
        for root_type in root_types:
            self.create(get_root(user_type, root_type))
        return self

    def delete(self, root_key: HKEYType):
        """ Delete the registry key at `root_key` """
        delete_item(root_key, self.item_reg_key)
        return self

    def delete_for(self, user_type: UserType, root_types: List[RootType]):
        for root_type in root_types:
            self.delete(get_root(user_type, root_type))
        return self


class PythonContextMenuItem(ContextMenuItem):
    def __init__(
            self,
            item_name: str,  # to be displayed in the contextmenu
            python_function: Callable,  # python function to be executed
            item_reg_key: str = "",  # key to be used in the registry
            icon: str = "",  # path to the icon to be shown along with item
            hide_terminal: bool = False,  # hide the python console on execution
            extended: bool = False  # if true, item will be shown with shift key
    ):
        if isfunction(python_function):
            script_path = Path(python_function.__code__.co_filename)
            script_folder = script_path.parent
            script_name = script_path.name.split(script_path.suffix)[0]
            function_name = python_function.__name__
            py_script = f"""import os, sys; os.chdir(r'{script_folder}'); __import__('{script_name}').{function_name}(sys.argv[1])"""
            py_executable = sys.executable.replace(
                "python.exe",
                "pythonw.exe") if hide_terminal else sys.executable
            command = f"""{py_executable} -c "{py_script}" "%V" """
            # print(command)
        else:
            raise TypeError(
                "Please pass a function type to python_function argument")
        super(PythonContextMenuItem, self).__init__(
            item_name, command, item_reg_key, icon, extended)


class ContextMenuGroup(object):
    def __init__(
            self,
            group_name: str,  # to be displayed in the contextmenu
            group_reg_key: str = "",  # key to be used in the registry
            icon: str = "",  # path to the icon to be shown along with item
            items: "List[Union[ContextMenuItem, ContextMenuGroup]]" = None,
            # items and subgroups to be shown
            extended: bool = False  # if true, item will be shown with shift key
    ):
        self.group_name = group_name
        self.group_reg_key = group_name if group_reg_key == "" else group_reg_key
        self.icon = icon
        self.items = []
        self.extended = extended
        if items is not None:
            self.add_items(items)

    def add_item(self, item: "Union[ContextMenuItem, ContextMenuGroup]"):
        assert isinstance(
            item, (ContextMenuItem, ContextMenuGroup)
        ), "Please pass instance of ContextMenuItem or ContextMenuGroup"
        self.items.append(item)
        return self

    def add_items(self,
                  items: "List[Union[ContextMenuItem, ContextMenuGroup]]"):
        assert isinstance(items, (
            tuple, list)), "Please provide an instance of tuple or list"
        for item in items:
            self.add_item(item)
        return self

    def create(self, root_key: HKEYType):
        """
        Adds entries into the registry for creating the item
        :param root_key: HKEYType key where the item is to be created.
                         Obtain the key using `get_root` function
        :return: Returns the ContextMenuGroup item
        """
        if is_cyclic_group(self):
            raise CyclicGroupException(
                "Congratulations! You're about to break your registry")
        group_key = CreateKey(root_key, self.group_reg_key)

        SetValueEx(group_key, "MUIVerb", 0, REG_SZ, self.group_name)
        SetValueEx(group_key, 'SubCommands', 0, REG_SZ, "")
        if self.icon != "":
            SetValueEx(group_key, "Icon", 0, REG_SZ, self.icon)
        if self.extended:
            SetValueEx(group_key, "Extended", 0, REG_SZ, "")

        subcommands_key = CreateKey(group_key, "shell")

        for item in self.items:
            item.create(subcommands_key)
        CloseKey(subcommands_key)
        CloseKey(group_key)
        return self

    def create_for(self, user_type: UserType, root_types: List[RootType]):
        for root_type in root_types:
            self.create(get_root(user_type, root_type))
        return self

    def delete(self, root_key: HKEYType):
        delete_item(root_key, self.group_reg_key)
        return self

    def delete_for(self, user_type: UserType, root_types: List[RootType]):
        for root_type in root_types:
            self.delete(get_root(user_type, root_type))
        return self


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
    if isinstance(root_type, str):
        root_type = type("root_type", (), {"value": root_type})
    if user_type is UserType.CURR_USER:
        root_type = r"Software\\Classes\\" + root_type.value
    else:
        root_type = root_type.value
    if "{FILE_TYPE}" in root_type:
        if file_type is None:
            raise ValueError(
                'Please provide a FILE_TYPE you want\n'
                'Usage example: get_root(user_type, RootType.FILE, r".zip")'
                'When using with `.create_for` methods, '
                'use RootType.FILE.format(FILE_TYPE = ".zip"')
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


def _del_key(rk: HKEYType):
    no_subkeys, _, __ = QueryInfoKey(rk)
    # print(no_subkeys)
    for i in range(no_subkeys):
        sk = EnumKey(rk, 0)
        # print(sk)
        _del_key(OpenKey(rk, sk))
    DeleteKey(rk, "")


def delete_item(root_key: HKEYType, item_reg_key: str):
    try:
        _del_key(OpenKey(root_key, item_reg_key))
    except FileNotFoundError:
        warnings.warn(
            "There is an error deleting the key, are you sure the key exists?")
    except:
        from traceback import print_exc
        print_exc()


def test_function(path_or_file_name):
    print("Path/file named selected", path_or_file_name)
    input("Press ENTER to continue")


if __name__ == '__main__':
    # add a menu for current user to be shown in directory background contextmenu
    user_root = get_root(UserType.CURR_USER, RootType.DIR_BG)

    # define complex nested contextmenu groups in a beautiful pythonic way
    cmgroup = ContextMenuGroup("Group 1", items = [  # first group
        ContextMenuItem("Item 1", "cmd.exe"),
        PythonContextMenuItem("Python fn", test_function),
        # execute a function function
        ContextMenuGroup("Group 2", items = [  # second group
            ContextMenuItem("Item 3", "cmd.exe"),
            ContextMenuItem("Item 4", "cmd.exe"),
            ContextMenuGroup("Group 3", items = [  # one more nested group
                ContextMenuItem("Item 5", "cmd.exe"),
                ContextMenuItem("Item 6", "cmd.exe")
            ])
        ])
    ]).create(user_root)

    # create the group to be shown at multiple locations easily
    cmgroup.create_for(UserType.CURR_USER, [RootType.DIR, RootType.ALL_FILES])
    input("Group 1 created, press ENTER to continue")

    # delete the menu created for DIB_BG location
    delete_item(user_root, cmgroup.group_reg_key)
    input("Group 1 deleted, press ENTER to close")

    # delete for other locations
    cmgroup.delete_for(UserType.CURR_USER, [RootType.DIR])

    # convert a python script to executable command using python_script_cmd function
    cmgroup = ContextMenuGroup("Group 1", items = [
        ContextMenuItem("Item 1", python_script_cmd(
            "example.py", rel_path = True)),
        ContextMenuItem("Item 2", python_script_cmd(
            "abc.py", rel_path = True))
    ]).create(
        get_root(UserType.CURR_USER, RootType.DIR_BG)
    ).create(
        get_root(UserType.CURR_USER, RootType.ALL_FILES)
    )
