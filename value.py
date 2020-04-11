from typing import Any, NamedTuple
from enum import Enum
import winreg


RegistryValueType = Enum('RegistryValueType', {name: value for name, value in winreg.__dict__.items() if name.startswith('REG_')})


class RegistryValue(NamedTuple):

    value: Any
    type_: RegistryValueType
