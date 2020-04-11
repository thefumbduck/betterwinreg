from __future__ import annotations
from typing import NewType, Any, Union, Sequence, Iterator
from pathlib import PurePath
import winreg

Hkey = NewType('Hkey', int)
RegistryPath = NewType('RegistryPath', PurePath)


class RegistryKey:

    hkey: Hkey
    path: RegistryPath

    @property
    def subkeys(self) -> Sequence[RegistryKey]:
        pass

    def __init__(self, path: Union[str, RegistryPath]) -> None:
        path = RegistryPath(path)

        hkey_str = path.parts[0]
        if not hkey_str.startswith('HKEY_') or not hasattr(winreg, hkey_str):
            raise OSError('The specified hkey is not valid')
        self.hkey = getattr(winreg, hkey_str)

        self.path = RegistryPath.joinpath(*path.parts[1:])

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
