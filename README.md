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

## Getting values

You can get a specific value by using a dict-like syntax:

```python
my_wacky_value = key['WackyValue']
```

You can also iterate though all the values a key has:

```python
for name, value in key:
    # do some more wacky stuff
```

Since working with the registry often requires knowing what you're doing with types, values are `RegistryValue`s, a named tuple that contains a `value` and a `type_` attribute.

For example, you would get the wallpaper path by doing:

```python
wallpaper_path = RegistryKey('HKEY_CURRENT_USER\Control Panel\Desktop')['WallPaper']
```

## Setting values

Setting values works in the same way:

```python
RegistryKey('HKEY_CURRENT_USER\Control Panel\Desktop')['WallPaper'] = r'D:\Pictures\wallpaper.png'
```
