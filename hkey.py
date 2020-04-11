from __future__ import annotations
import winreg


class Hkey:

    name: str
    id_: int

    def __init__(self, name: str) -> Hkey:
        self.name = name

        if not name.startswith('HKEY_') or not hasattr(winreg, name):
            raise OSError('The specified hkey is not valid')
        self.id_ = getattr(winreg, name)
