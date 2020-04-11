import winreg
from enum import IntEnum
from typing import Any, NamedTuple


# Manually write these to have autocomplete
class RegistryValueType(IntEnum):
    BINARY = winreg.REG_BINARY
    DWORD = winreg.REG_DWORD
    DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    QWORD = winreg.REG_QWORD
    QWORD_LITTLE_ENDIAN = winreg.REG_QWORD_LITTLE_ENDIAN
    EXPAND_SZ = winreg.REG_EXPAND_SZ
    LINK = winreg.REG_LINK
    MULTI_SZ = winreg.REG_MULTI_SZ
    NONE = winreg.REG_NONE
    RESOURCE_LIST = winreg.REG_RESOURCE_LIST
    FULL_RESOURCE_DESCRIPTOR = winreg.REG_FULL_RESOURCE_DESCRIPTOR
    RESOURCE_REQUIREMENTS_LIST = winreg.REG_RESOURCE_REQUIREMENTS_LIST
    SZ = winreg.REG_SZ


class RegistryValue(NamedTuple):

    value: Any
    type_: RegistryValueType
