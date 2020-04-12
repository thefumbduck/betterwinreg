from betterwinreg.value import get_registry_instance, RegistryValueType, Dword, Qword, Sz, ExpandSz, MultiSz


class TestConversion:

    def test_int(self):
        assert isinstance(get_registry_instance(42, RegistryValueType.DWORD), Dword)
        assert isinstance(get_registry_instance(42, RegistryValueType.QWORD), Qword)

    def test_str(self):
        assert isinstance(get_registry_instance('hi', RegistryValueType.SZ), Sz)
        assert isinstance(get_registry_instance('hi', RegistryValueType.EXPAND_SZ), ExpandSz)
        assert isinstance(get_registry_instance('hi', RegistryValueType.MULTI_SZ), MultiSz)

    def test_none(self):
        assert get_registry_instance(None, RegistryValueType.NONE) is None
