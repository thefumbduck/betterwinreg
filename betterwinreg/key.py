from __future__ import annotations

import winreg
from enum import IntEnum
from pathlib import PureWindowsPath
from typing import Any, Iterator, Union

from hkey import Hkey
from value import RegistryValue, RegistryValueType


class RegistryPath(PureWindowsPath):
    pass


class RegistryKey:

    class EnumValueReturnMembers(IntEnum):
        NAME = 0
        VALUE = 1
        TYPE = 2

    class QueryInfoReturnMembers(IntEnum):
        SUBKEYS_AMOUNT = 0
        VALUES_AMOUNT = 1
        LAST_MODIFICATION = 2

    class QueryValueReturnMembers(IntEnum):
        VALUE = 0
        TYPE = 1

    hkey: Hkey
    path: RegistryPath

    @property
    def full_path(self) -> RegistryPath:
        return RegistryPath(self.hkey.name) / self.path
    
    @property
    def parent(self) -> RegistryKey:
        return RegistryKey.from_hkey_and_path(self.hkey, self.path.parent)

    @property
    def subkeys(self) -> Iterator[RegistryKey]:
        from itertools import count

        handle = self.make_handle(True)

        try:
            for i in count():
                key_name = winreg.EnumKey(handle, i)
                key = RegistryKey.from_hkey_and_path(
                    self.hkey, self.path / key_name)
                yield key
        except OSError:
            return

    def __init__(self, path: Union[str, RegistryPath] = None) -> None:
        if not path:
            return

        path = RegistryPath(path)

        # If path starts with 'Computer/', we remove it to standardize it
        path_parts = path.parts
        if path_parts[0] == 'Computer':
            path_parts = path_parts[1:]

        self.hkey = Hkey(path_parts[0])
        self.path = RegistryPath().joinpath(*path_parts[1:])

    @staticmethod
    def from_hkey_and_path(hkey: Hkey, path: RegistryPath) -> RegistryKey:
        key = RegistryKey()
        key.hkey = hkey
        key.path = path
        return key

    def create(self) -> None:
        winreg.CreateKeyEx(self.hkey.id_, str(self.path), 0)

    def delete(self, recursive: bool = True) -> None:
        if recursive:
            for subkey in self.subkeys:
                subkey.delete()
        winreg.DeleteKeyEx(self.hkey.id_, str(self.path))

    def make_handle(self, readonly: bool = True) -> winreg.HKEYType:
        access = winreg.KEY_READ if readonly else winreg.KEY_ALL_ACCESS
        return winreg.OpenKeyEx(self.hkey.id_, str(self.path), 0, access)

    def __len__(self) -> int:
        return winreg.QueryInfoKey(self.make_handle(True))[self.QueryInfoReturnMembers.VALUES_AMOUNT]

    def __iter__(self) -> Iterator[RegistryValue]:
        from itertools import count

        handle = self.make_handle(True)

        try:
            for i in count():
                data = winreg.EnumValue(handle, i)
                type_ = RegistryValueType(
                    data[self.EnumValueReturnMembers.TYPE])
                yield (data[self.EnumValueReturnMembers.NAME], RegistryValue(data[self.EnumValueReturnMembers.VALUE], type_))
        except OSError:
            return

    def __getitem__(self, key: str) -> RegistryValue:
        data = winreg.QueryValueEx(self.make_handle(True), key)
        type_ = RegistryValueType(data[self.QueryValueReturnMembers.TYPE])
        return RegistryValue(data[self.QueryValueReturnMembers.VALUE], type_)

    def __setitem__(self, key: str, value: RegistryValue) -> None:
        winreg.SetValueEx(self.make_handle(False), key,
                          0, value.type_, value.value)

    def __delitem__(self, key: str) -> None:
        winreg.DeleteValue(self.make_handle(False), key)

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self.full_path)})'