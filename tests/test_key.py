from betterwinreg.key import RegistryKey, RegistryPath


class TestKeyParsing:

    def test_hkey(self):
        assert RegistryKey(r'HKEY_CLASSES_ROOT\Directory\shell').hkey.name == 'HKEY_CLASSES_ROOT'
    
    def test_path(self):
        assert RegistryKey(r'HKEY_CLASSES_ROOT\Directory\shell').path == RegistryPath(r'Directory\shell')
    
    def test_computer_prefix(self):
        assert RegistryKey(r'Computer\HKEY_CLASSES_ROOT\Directory\shell').hkey
