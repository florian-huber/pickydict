from collections import UserDict


class PickyDict(UserDict):
    """More picky version of Python dictionary.

    PickyDict objects will behave just like Python dictionaries, with a few
    notable exceptions:
        (1) PickyDict has a force_lower_case attribute. If set to True (default)
        then dictionary keys will all be treated as lower-case.
        (2) PickyDict can contain a second dictionary named "replacements" with
        mappings to enforce translating specific key words.

    Examples:

    .. code-block:: python

        # per default force_lower_case is set to True:
        my_dict = PickyDict({"A": 1, "B": 2})
        print(my_dict)  # => {'a': 1, 'b': 2}

        # now also using a replacements dictionary
        my_dict = PickyDict({"A": 1, "B": 2},
                            replacements={"a": "abc", "b": "bcd", "c": "cde"})
        print(my_dict)  # => {'abc': 1, 'bcd': 2}
        my_dict["c"] = 100
        print(my_dict)  # => {'abc': 1, 'bcd': 2, , 'cde': 100}
        my_dict["b"] = 5  # => ValueError: Key 'b' will be interpreted as 'bcd'...

    """
    def __init__(self, input_dict: dict = None,
                 replacements: dict = None,
                 force_lower_case: bool = True):
        """
        Parameters
        ----------
        input_dict : dict, optional
            This is the actual dictionary within PickyDict. 
        replacements : dict, optional
            This is second dictionary within PickyDict containing mappings of all
            keys which the user wants to force into a specific form (see code example).
        force_lower_case : bool, optional
            If set to True (default) all dictionary keys will be forced to be lower case.
        """
        self._force_lower_case = force_lower_case
        self._replacements = replacements
        if input_dict is not None:
            UserDict.__init__(self, input_dict)
        else:
            UserDict.__init__(self)

    def __setitem__(self, key, value):
        if self._force_lower_case:
            key = key.lower()
        if self._replacements is not None and key in self._replacements:
            proper_key = self._replacements[key]
            if self.data.get(proper_key, None) is not None:
                raise ValueError(f"Key '{key}' will be interpreted as '{proper_key}'. "
                                 "But this entry already exists. "
                                 f"Please use '{proper_key}' if you want to replace the entry.")
            self.data[proper_key] = value
        else:
            self.data[key] = value

    def set_pickyness(self, replacements: dict, force_lower_case: bool):
        self._force_lower_case = force_lower_case
        self._replacements = replacements

    def _apply_replacements(self):
        for key, value in self.data.items():
            if self._replacements is not None and key in self._replacements:
                proper_key = self._replacements[key]
                if self.data.get(proper_key, None) is not None:
                    raise ValueError("Conflicting entries found. "
                                     f"Key '{key}' will now be interpreted as '{proper_key}'. "
                                     "But the dictionary already contains a value for this key.")
                else:
                    self.data[proper_key] = value
                    self.data.pop(key)

    @property
    def replacements(self):
        return self._replacements.copy()

    @replacements.setter
    def replacements(self, new_replacements):
        self._replacements = new_replacements