from betterwinreg.value import get_instance, RegistryValueType, Dword, Qword, Sz


class TestConversion:

    def test_int(self):
        assert isinstance(get_instance(42, RegistryValueType.DWORD), Dword)
        assert isinstance(get_instance(42, RegistryValueType.QWORD), Qword)

    def test_str(self):
        assert isinstance(get_instance('hi', RegistryValueType.SZ), Sz)
