from betterwinreg.value import get_registry_instance, RegistryValueType, Dword, DwordBigEndian, Qword, Sz, ExpandSz, MultiSz


class TestConversion:

    def test_int(self):
        assert isinstance(get_registry_instance(42, RegistryValueType.DWORD), Dword)
        assert isinstance(get_registry_instance(42, RegistryValueType.QWORD), Qword)

    def test_str(self):
        assert isinstance(get_registry_instance('hi', RegistryValueType.SZ), Sz)
        assert isinstance(get_registry_instance('hi', RegistryValueType.EXPAND_SZ), ExpandSz)
        assert isinstance(get_registry_instance(['hello', 'world'], RegistryValueType.MULTI_SZ), MultiSz)

    def test_none(self):
        assert get_registry_instance(None, RegistryValueType.NONE) is None

    def test_weird(self):
        assert isinstance(get_registry_instance(b'abc', RegistryValueType.DWORD_BIG_ENDIAN), DwordBigEndian)


class TestMisc:

    def test_repr(self):
        assert repr(Dword(42)) == 'Dword(42)'
        assert repr(Sz('Hi')) == "Sz('Hi')"

    def test_str(self):
        assert str(Dword(42)) == '42'
        assert str(Sz('Hi')) == 'Hi'
