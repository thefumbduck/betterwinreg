from __future__ import annotations

import winreg


class Hkey:

    name: str
    id_: int

    def __init__(self, name: str) -> Hkey:
        self.name = name

        if not self.is_valid(name):
            raise OSError('The specified hkey is not valid')
        self.id_ = getattr(winreg, name)

    @staticmethod
    def is_valid(name: str) -> bool:
        return name.startswith('HKEY_') and hasattr(winreg, name)
