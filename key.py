from __future__ import annotations
from typing import NewType, Any, Union, Iterator
from pathlib import PureWindowsPath
import winreg

from hkey import Hkey


class RegistryPath(PureWindowsPath):
    pass


class RegistryKey:

    hkey: Hkey
    path: RegistryPath

    @property
    def full_path(self) -> RegistryPath:
        return RegistryPath(self.hkey.name) / self.path

    @property
    def subkeys(self) -> Iterator[RegistryKey]:
        from itertools import count
        
        try:
            for i in count():
                key_name = winreg.EnumKey(self.make_handle(), i)
                key = RegistryKey.from_hkey_and_path(self.hkey, self.path / key_name)
                yield key
        except OSError:
            return

    def __init__(self, path: Union[str, RegistryPath]=None) -> None:
        if not path:
            return

        path = RegistryPath(path)

        self.hkey = Hkey(path.parts[0])
        self.path = RegistryPath().joinpath(*path.parts[1:])
    
    @staticmethod
    def from_hkey_and_path(hkey: Hkey, path: RegistryPath) -> RegistryKey:
        key = RegistryKey()
        key.hkey = hkey
        key.path = path
        return key

    def delete(self, recursive: bool=True) -> None:
        if recursive:
            for subkey in self.subkeys:
                subkey.delete()
        winreg.DeleteKeyEx(self.hkey.id_, str(self.path))

    def make_handle(self) -> winreg.HKEYType:
        return winreg.OpenKeyEx(self.hkey.id_, str(self.path))

    def __len__(self) -> int:
        pass

    def __getitem__(self, key: str) -> Any:
        pass

    def __setitem__(self, key: str, value: Any) -> None:
        pass

    def __delitem__(self, key: str) -> None:
        pass

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self.full_path)})'
