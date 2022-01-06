from collections import UserDict
import re


class PickyDict(UserDict):
    """More picky version of Python dictionary.

    PickyDict objects will behave just like Python dictionaries, with a few
    notable exceptions:
        (1) PickyDict has a force_lower_case attribute. If set to True (default)
        then dictionary keys will all be treated as lower-case.
        (2) PickyDict can contain a second dictionary named "key_replacements" with
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
        print(my_dict)  # => {'abc': 1, 'bcd': 2, 'cde': 100}
        my_dict["b"] = 5  # => ValueError: Key 'b' will be interpreted as 'bcd'...

    """
    def __init__(self, input_dict: dict = None,
                 key_replacements: dict = None,
                 key_regex_replacements: dict = None,
                 force_lower_case: bool = True):
        """
        Parameters
        ----------
        input_dict : dict, optional
            This is the actual dictionary within PickyDict.
        key_replacements : dict, optional
            This additional dictionary within PickyDict contains mappings of all
            keys which the user wants to force into a specific form (see code example).
        key_regex_replacements : dict, optional
            This additional dictionary contains pairs of regex (regular expression) strings
            and replacement strings to clean and harmonize the main dictionary keys.
            An example would be {r"\s": "_"} which will replace all spaces with underscores.
        force_lower_case : bool, optional
            If set to True (default) all dictionary keys will be forced to be lower case.
        """
        self._force_lower_case = force_lower_case
        self._key_replacements = key_replacements
        self._key_regex_replacements = key_regex_replacements
        if input_dict is not None:
            UserDict.__init__(self, input_dict)
        else:
            UserDict.__init__(self)

    def __setitem__(self, key, value):
        proper_key = self._harmonize_key(key)
        if key == proper_key:
            self.data[key] = value
        elif self.data.get(proper_key, None) is not None:
            raise ValueError(f"Key '{key}' will be interpreted as '{proper_key}'. "
                             "But this entry already exists. "
                             f"Please use '{proper_key}' if you want to replace the entry.")
        else:
            self.data[proper_key] = value

    def set_pickyness(self, key_replacements: dict = None,
                      key_regex_replacements: dict = None,
                      force_lower_case: bool = True):
        """
        Function to set the pickyness of the dictionary.
        Will automatically also run the new replacements if the dictionary already exists.

        Parameters
        ----------
        key_replacements : dict, optional
            This is second dictionary within PickyDict containing mappings of all
            keys which the user wants to force into a specific form (see code example).
        key_regex_replacements : dict, optional
            This additional dictionary contains pairs of regex (regular expression) strings
            and replacement strings to clean and harmonize the main dictionary keys.
            An example would be {r"\s": "_"} which will replace all spaces with underscores.
        force_lower_case : bool, optional
            If set to True (default) all dictionary keys will be forced to be lower case.
        """
        self._force_lower_case = force_lower_case
        self._key_replacements = key_replacements
        self._key_regex_replacements = key_regex_replacements
        self._apply_replacements()
        

    def _harmonize_key(self, key):
        """Applies lower-case, then regex replacements, then key replacements."""
        if self._force_lower_case:
            key = key.lower()
        if self._key_regex_replacements is not None:
            for regex_pattern, target in self._key_regex_replacements.items():
                key = re.sub(regex_pattern, target, key)
        if self._key_replacements is not None and key in self._key_replacements:
            key = self._key_replacements[key]
        return key

    def _apply_replacements(self):
        """Harmonizes all keys in dictionary."""
        keys_initial = self.data.copy().keys()
        for key in keys_initial:
            proper_key = self._harmonize_key(key)
            if key != proper_key and self.data.get(proper_key, None) is not None:
                raise ValueError(f"Key '{key}' will be interpreted as '{proper_key}'. "
                                 "But this entry already exists. "
                                 f"Please use '{proper_key}' if you want to replace the entry.")
            if key != proper_key:
                self.data[proper_key] = self.data[key]
                self.data.pop(key)

    @property
    def force_lower_case(self):
        return self._force_lower_case.copy()

    @force_lower_case.setter
    def force_lower_case(self, new_force_lower_case):
        self._force_lower_case = new_force_lower_case
        self._apply_replacements()

    @property
    def key_replacements(self):
        return self._key_replacements.copy()

    @key_replacements.setter
    def key_replacements(self, new_key_replacements):
        self._key_replacements = new_key_replacements
        self._apply_replacements()

    @property
    def key_regex_replacements(self):
        return self._key_regex_replacements.copy()

    @key_regex_replacements.setter
    def key_regex_replacements(self, new_key_regex_replacements):
        self._key_regex_replacements = new_key_regex_replacements
        self._apply_replacements()
