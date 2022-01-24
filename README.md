![GitHub](https://img.shields.io/github/license/florian-huber/pickydict)
[![PyPI](https://img.shields.io/pypi/v/pickydict)](https://pypi.org/project/pickydict/)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/florian-huber/pickydict/CI_Build)

# pickydict - the more picky version of Python dictionary

`PickyDict` objects will behave just like Python dictionaries, with a few
notable exceptions:

1. PickyDict has a `force_lower_case` attribute.   
If set to True (default) then dictionary keys will all be treated as lower-case.

2. PickyDict can contain two additional dictionaries named `key_replacements`
    and `key_regex_replacements` with mappings to enforce translating specific key words.

## Installation

PickyDict can simply be installed with:
```
pip install pickydict
```

It has no further dependencies and should run fine with Python >= 3.6 (probably also lower versions, but that is not tested).

## Code examples

```python
from pickydict import PickyDict

# per default force_lower_case is set to True:
my_dict = PickyDict({"A": 1, "B": 2})
print(my_dict)  # => {'a': 1, 'b': 2}

# now also using a replacements dictionary
my_dict = PickyDict({"A": 1, "B": 2},
                    key_replacements={"a": "abc", "b": "bcd", "c": "cde"})
print(my_dict)  # => {'abc': 1, 'bcd': 2}

# When adding a value using an undesired key, the key will automatically be fixed
my_dict["c"] = 100
print(my_dict)  # => {'abc': 1, 'bcd': 2, 'cde': 100}

# Trying to add a value using an undesired key while the proper key already exists,
# will raise an exception.
my_dict["b"] = 5  # => ValueError: Key 'b' will be interpreted as 'bcd'...
```

It is also possible to add a dictionary with regex expression to replace parts of
key strings. This is done using the `key_regex_replacements` attribute. In the following example the dictionary will replace all spaces in keys with underscores.

Important to note is that regex based replacements will be carried out **before** the more specific key_replacements. This is to reduce the number of possible variations and make things simpler for the user.

Example:

```python
from pickydict import PickyDict

my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"},
                    key_replacements={"last_name": "surname"},
                    key_regex_replacements={r"\s": "_"})
print(my_dict)  # => {'first_name': 'Peter', 'surname': 'Petersson'}
```

Whenever the pickyness is updated, no matter if the `force_lower_case`, `key_replacements`,
or `key_regex_replacements`, the entire dictionary will be updated accoringly.

Example:

```python

from pickydict import PickyDict

my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"})
print(my_dict)  # => {'first name': 'Peter', 'last name': 'Petersson'}

my_dict.set_pickyness(key_replacements={"last_name": "surname"},
                      key_regex_replacements={r"\s": "_"})
print(my_dict)  # => {'first_name': 'Peter', 'surname': 'Petersson'}
```

## For the rest it's just a `dict`
All other operation should work as you are used to from Python dictionaries.
