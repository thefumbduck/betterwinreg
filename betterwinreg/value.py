import winreg
from enum import IntEnum
from typing import Any


# Manually write these to have autocomplete
class RegistryValueType(IntEnum):
    BINARY = winreg.REG_BINARY
    DWORD = winreg.REG_DWORD
    DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
    QWORD = winreg.REG_QWORD
    QWORD_LITTLE_ENDIAN = winreg.REG_QWORD_LITTLE_ENDIAN
    SZ = winreg.REG_SZ
    EXPAND_SZ = winreg.REG_EXPAND_SZ
    MULTI_SZ = winreg.REG_MULTI_SZ
    LINK = winreg.REG_LINK
    NONE = winreg.REG_NONE
    RESOURCE_LIST = winreg.REG_RESOURCE_LIST
    FULL_RESOURCE_DESCRIPTOR = winreg.REG_FULL_RESOURCE_DESCRIPTOR
    RESOURCE_REQUIREMENTS_LIST = winreg.REG_RESOURCE_REQUIREMENTS_LIST


class RegistryValue:
    winreg_type: RegistryValueType = None


class Binary(RegistryValue, bytes):
    winreg_type: RegistryValueType = RegistryValueType.BINARY


class Dword(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.DWORD


class DwordBigEndian(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.DWORD_BIG_ENDIAN


class Qword(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.QWORD


class QwordLittleEndian(RegistryValue, int):
    winreg_type: RegistryValueType = RegistryValueType.QWORD_LITTLE_ENDIAN


class Sz(RegistryValue, str):
    winreg_type: RegistryValueType = RegistryValueType.SZ


class ExpandSz(RegistryValue, str):
    winreg_type: RegistryValueType = RegistryValueType.EXPAND_SZ


class MultiSz(RegistryValue, str):
    winreg_type: RegistryValueType = RegistryValueType.MULTI_SZ


class Link(RegistryValue, bytes):
    winreg_type: RegistryValueType = RegistryValueType.LINK


class ResourceList(RegistryValue, bytes):
    winreg_type: RegistryValueType = RegistryValueType.RESOURCE_LIST


class FullResourceDescriptor(RegistryValue, bytes):
    winreg_type: RegistryValueType = RegistryValueType.FULL_RESOURCE_DESCRIPTOR


class ResourceRequirementsList(RegistryValue, bytes):
    winreg_type: RegistryValueType = RegistryValueType.RESOURCE_REQUIREMENTS_LIST
