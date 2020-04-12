import winreg

from betterwinreg.hkey import Hkey


def test_id():
    hkey = Hkey('HKEY_CURRENT_USER')
    assert hkey.id_ == winreg.HKEY_CURRENT_USER


def test_abbreviated_name():
    assert Hkey('HKEY_CURRENT_USER') == Hkey('HKCU')
