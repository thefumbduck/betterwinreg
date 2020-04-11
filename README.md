# better-winreg

A wrapper that makes working with winreg easier.

## Getting a RegistryKey instance

To get a `RegistryKey` instance, simply do:

```python
from betterwinreg.key import RegistryKey
key = RegistryKey('HKEY_MY_HKEY/Path/To/Key/You/Want')
```

You can also use backslashes:

```python
key = RegistryKey('HKEY_MY_KEY\\Path\\To\\Key\\You\\Want')
```

Or, if you don't want to escape every backslash, you can use raw strings:

```python
key = RegistryKey(r'HKEY_MY_KEY\Path\To\Key\You\Want')
```
