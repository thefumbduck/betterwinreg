from betterwinreg.key import RegistryKey, RegistryPath
from betterwinreg.value import RegistryValue, RegistryValueType


class TestKeyParsing:

    def test_hkey(self):
        assert RegistryKey(r'HKEY_CLASSES_ROOT\Directory\shell').hkey.name == 'HKEY_CLASSES_ROOT'

    def test_path(self):
        assert RegistryKey(r'HKEY_CLASSES_ROOT\Directory\shell').path == RegistryPath(r'Directory\shell')

    def test_computer_prefix(self):
        assert RegistryKey(r'Computer\HKEY_CLASSES_ROOT\Directory\shell').hkey


class TestKeyManipulation:

    SET_TEST_KEY_PATH = r'HKEY_CURRENT_USER\harmless_test'

    def test_get(self):
        assert RegistryKey(r'Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer')['UserSignedIn'].value == 1

    def test_set_value(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['test'] = RegistryValue(42, RegistryValueType.DWORD)
        key.flush()
        assert key['test'].value == 42

    def test_del_value(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['test'] = RegistryValue(42, RegistryValueType.DWORD)
        key.flush()
        del key['test']
        key.flush()
        assert 'test' not in key

    def test_del_key(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        if not key.is_key():
            key.create()
        key.flush()
        key.delete()
        assert not key.is_key()
