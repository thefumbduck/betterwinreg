from typing import Any, NamedTuple
from enum import Enum
import winreg

VALID_VALUE_TYPE_NAMES = [
    'BINARY', 'DWORD', 'DWORD_BIG_ENDIAN', 'QWORD', 'QWORD_LITTLE_ENDIAN','QWORD', 'QWORD_LITTLE_ENDIAN',
    'EXPAND_SZ', 'LINK', 'MULTI_SZ', 'NONE', 'RESOURCE_LIST', 'FULL_RESOURCE_DESCRIPTOR', 'RESOURCE_REQUIREMENTS_LIST', 'SZ'
]

RegistryValueType = Enum('RegistryValueType', {name: value for name, value in winreg.__dict__.items() if name[4:] in VALID_VALUE_TYPE_NAMES})


class RegistryValue(NamedTuple):

    value: Any
    type_: RegistryValueType
