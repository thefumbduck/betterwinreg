from typing import NewType, Union
from pathlib import PurePath

Hkey = NewType('Hkey', int)
RegistryPath = NewType('RegistryPath', PurePath)


class RegistryKey:

    hkey: Hkey
    path: RegistryPath

    def __init__(self, path: Union[str, RegistryPath]):
        pass
