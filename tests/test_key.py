import pytest
from betterwinreg.key import RegistryKey, RegistryPath
from betterwinreg.value import RegistryValue, RegistryValueType, Dword


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
        assert RegistryKey(r'Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer')['UserSignedIn'] == 1

    def test_get_fail(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        if not key.is_key():
            key.create()
        with pytest.raises(KeyError):
            key['InvalidKey']
        key.delete()

    def test_create(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        if key.is_key():
            key.delete()
        key.create()
        assert key.is_key()
        key.delete()

    def test_set_value(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['test'] = Dword(42)
        key.flush()
        assert key['test'] == 42

    def test_del_value(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['test'] = Dword(42)
        key.flush()
        del key['test']
        key.flush()
        assert 'test' not in key.values()

    def test_default_value(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)

        key.default_value = Dword(42)
        assert key.has_default_value()
        assert key.default_value == key[''] == 42

        del key.default_value
        assert not key.has_default_value()
        assert '' not in key.values()

        key.delete()

    def test_del_key(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        if not key.is_key():
            key.create()
        key.flush()
        key.delete()
        assert not key.is_key()

    def test_values_iter(self):
        import re

        key = RegistryKey(self.SET_TEST_KEY_PATH)

        for i in range(10):
            key[f'test{i}'] = Dword(i)
        key.flush()

        values = key.values()
        assert len(values) > 0
        for name, value in values.items():
            assert re.match(r'test([0-9])+', name) and isinstance(value, int)

        key.delete()

    def test_key_len(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)

        for i in range(10):
            key[f'test{i}'] = Dword(i)

        assert len(key) == 10

        key.delete()

    def test_set_get_none(self):
        key = RegistryKey(self.SET_TEST_KEY_PATH)
        key['TestNone'] = None
        assert key['TestNone'] is None
        key.delete()

    def test_copy(self):
        key = RegistryKey(r'HKCU\harmless_key')
        if not key.is_key():
            key.create()

        key['valuetest'] =  Dword(7)
        (key / 'test1').create()
        (key / 'test1')['valuetest'] = Dword(42)

        new_key = key.parent / 'harmless2'
        key.copy(new_key)

        assert new_key['valuetest'] == 7
        assert (new_key / 'test1')['valuetest'] == 42

        key.delete()
        new_key.delete()

    def test_rename(self):
        key = RegistryKey(r'HKCU\harmless_key')
        key2 = RegistryKey(r'HKCU\harmless2')

        key['valuetest'] =  Dword(7)
        (key / 'test1').create()
        (key / 'test1')['valuetest'] = Dword(42)

        key.rename(key2)

        assert not key.is_key()
        assert key2.is_key()

        with pytest.raises(ValueError):
            key2.rename(key2 / 'subkey')

        key2.delete()


class TestKeyNavigation:

    def test_eq(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test') == RegistryKey(r'HKEY_CURRENT_USER/harmless_test')

    def test_ne(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test') != RegistryKey(r'HKEY_CURRENT_USER\harmful_test')

    def test_parent(self):
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test\subkey').parent == RegistryKey(r'HKEY_CURRENT_USER\harmless_test')
        assert RegistryKey(r'HKEY_CURRENT_USER\harmless_test').parent == RegistryKey(r'HKEY_CURRENT_USER')

    def test_key_name(self):
        assert RegistryKey(r'HKCU\test').name == 'test'

    def test_subkeys(self):
        key = RegistryKey(r'HKEY_CURRENT_USER\harmless_key')
        if not key.is_key():
            key.create()

        (key / 'test1').create()
        (key / 'test2').create()

        assert len(key.subkeys()) == 2

        key.delete()

    def test_walk(self):
        key = RegistryKey(r'HKCU\harmless_key')
        if not key.is_key():
            key.create()

        (key / 'test1').create()
        (key / 'test1/test11').create()
        (key / 'test1/test12').create()
        (key / 'test2').create()
        (key / 'test2/test21').create()

        walk_results = list(key.walk())
        expected_results = [
            (key, ['test1', 'test2']),
            (key / 'test1', ['test11', 'test12']),
            (key / 'test2', ['test21']),
        ]

        for actual, expected in zip(walk_results, expected_results):
            assert actual == expected

        key.delete()


class TestKeyMisc:

    def test_repr(self):
        assert repr(RegistryKey(r'HKEY_CURRENT_USER\harmless_test')) == r"RegistryKey('HKEY_CURRENT_USER\harmless_test')"

    def test_str(self):
        assert str(RegistryKey(r'HKEY_CURRENT_USER\harmless_test')) == r'HKEY_CURRENT_USER\harmless_test'
