from __future__ import annotations
from typing import NewType, Any, Union, Iterator
from pathlib import PureWindowsPath
import winreg

Hkey = NewType('Hkey', int)


class RegistryPath(PureWindowsPath):
    pass


class RegistryKey:

    hkey: Hkey
    path: RegistryPath

    @property
    def handle(self) -> winreg.HKEYType:
        return winreg.OpenKeyEx(self.hkey, str(self.path))

    @property
    def subkeys(self) -> Iterator[RegistryKey]:
        from itertools import count
        
        try:
            for i in count():
                key_name = winreg.EnumKey(self.handle, i)
                key = RegistryKey.from_hkey_and_path(self.hkey, self.path / key_name)
                yield key
        except OSError:
            return

    def __init__(self, path: Union[str, RegistryPath]=None) -> None:
        if not path:
            return
        
        path = RegistryPath(path)

        hkey_str = path.parts[0]
        if not hkey_str.startswith('HKEY_') or not hasattr(winreg, hkey_str):
            raise OSError('The specified hkey is not valid')
        self.hkey = getattr(winreg, hkey_str)

        self.path = RegistryPath().joinpath(*path.parts[1:])
    
    @staticmethod
    def from_hkey_and_path(hkey: Hkey, path: RegistryPath) -> RegistryKey:
        key = RegistryKey()
        key.hkey = hkey
        key.path = path
        return key

    def delete(self) -> None:
        pass

    def __len__(self) -> int:
        pass

    def __getitem__(self, key: str) -> Any:
        pass

    def __setitem__(self, key: str, value: Any) -> None:
        pass

    def __delitem__(self, key: str) -> None:
        pass
