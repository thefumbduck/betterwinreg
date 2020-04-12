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

    def test_existence(self):
        assert RegistryKey(r'Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer').is_key()
        assert not RegistryKey(r'HKEY_CURRENT_USER\ThisKeyDoesntExist').is_key()

    def test_get(self):
        assert RegistryKey(r'Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer')['UserSignedIn'].value == 1

    def test_create(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        if key.is_key():
            key.delete()
        key.create()
        assert key.is_key()
        key.delete()

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

    def test_key_len(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)

        for i in range(10):
            key[f'test{i}'] = RegistryValue(i, RegistryValueType.DWORD)

        assert len(key) == 10

        key.delete()

    def test_key_contains(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['test1'] = RegistryValue(42, RegistryValueType.DWORD)
        assert 'test1' in key
        key.delete()


class TestKeyNavigation:

    def test_eq(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test') == RegistryKey(r'HKEY_CURRENT_USER/harmless_test')

    def test_ne(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test') != RegistryKey(r'HKEY_CURRENT_USER\harmful_test')

    def test_parent(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test\subkey').parent == RegistryKey(r'HKEY_CURRENT_USER\harmless_test')
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test').parent == RegistryKey(r'HKEY_CURRENT_USER')

    def test_subkeys(self):
        key = RegistryKey(r'HKEY_CURRENT_USER\harmless_key')
        if not key.is_key():
            key.create()

        (key / 'test1').create()
        (key / 'test2').create()

        assert len(list(key.subkeys)) == 2

        key.delete()


class TestKeyMisc:

    def test_repr(self):
        assert repr(RegistryKey(r'HKEY_CURRENT_USER\harmless_test')) == r"RegistryKey('HKEY_CURRENT_USER\harmless_test')"
