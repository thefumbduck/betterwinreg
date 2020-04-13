# better-winreg

A sane way of working with the Windows registry.

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

## Getting values

You can get a specific value by using a dict-like syntax:

```python
my_wacky_value = key['WackyValue']
```

You can also iterate though all the values a key has:

```python
for name, value in key.values().items():
    # do some more wacky stuff
```

For example, you would get the wallpaper path by doing:

```python
wallpaper_path = RegistryKey(r'HKEY_CURRENT_USER\Control Panel\Desktop')['WallPaper']
```

## Setting and deleting values

Since registry types are different than Python types, you need to specify what type the registry value will be set to.

```python
from betterwinreg.value import Sz
RegistryKey(r'HKEY_CURRENT_USER\Control Panel\Desktop')['WallPaper'] = Sz(r'D:\Pictures\wallpaper.png')
```

To delete a value, you can use `del`:

```python
del RegistryKey(r'HKEY_CLASSES_ROOT\Directory\Shell\git_shell')['WallPaper']
```

## Navigating through the registry

The main ways to move through the registry are using `subkeys()` and `parent`, and concatenating in a Path-like way.

```python
>>> RegistryKey(r'HKEY_CURRENT_USER\Control Panel\Desktop').parent
RegistryKey('HKEY_CURRENT_USER\Control Panel')

>>> RegistryKey(r'HKEY_CURRENT_USER\Control Panel\Desktop').subkeys()
[RegistryKey(r'HKEY_CURRENT_USER\Control Panel\Desktop\Colors'), RegistryKey('HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics'), RegistryKey('HKEY_CURRENT_USER\Control Panel\Desktop\MuiCached')]
```

You can also join `RegistryKey`s in a `Path`-like manner:

```python
>>> RegistryKey(r'HKEY_CURRENT_USER\Control Panel') / 'Desktop'
RegistryKey('HKEY_CURRENT_USER\Control Panel\Desktop')
```
