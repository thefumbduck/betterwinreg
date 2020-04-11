from typing import NewType, Any, Union, Sequence, Iterator
from pathlib import PurePath

Hkey = NewType('Hkey', int)
RegistryPath = NewType('RegistryPath', PurePath)


class RegistryKey:

    hkey: Hkey
    path: RegistryPath


    @property
    def subkeys(self) -> Sequence[RegistryKey]:
        pass


    def __init__(self, path: Union[str, RegistryPath]) -> None:
        pass


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
