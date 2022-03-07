import logging
import json
import re


logger = logging.getLogger('pickydict')


class PickyDict(dict):
    """More picky version of Python dictionary.

    PickyDict objects will behave just like Python dictionaries, with a few
    notable exceptions:
        (1) PickyDict has a force_lower_case attribute. If set to True (default)
        then dictionary keys will all be treated as lower-case.
        (2) PickyDict can contain two additional dictionaries named "key_replacements"
        and "key_regex_replacements with mappings to enforce translating specific key words.

    Examples:

    .. code-block:: python

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


    It is also possible to add a dictionary with regex expression to replace parts of
    key strings. This is done using the key_regex_replacements attribute.

    Example:

    .. code-block:: python

        from pickydict import PickyDict

        my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"},
                            key_replacements={"last_name": "surname"},
                            key_regex_replacements={r"\\s": "_"})
        print(my_dict)  # => {'first_name': 'Peter', 'surname': 'Petersson'}


    Whenever the pickyness is updated, no matter if the force_lower_case, key_replacements,
    or key_regex_replacements, the entire dictionary will be updated accoringly.

    Example:

    .. code-block:: python

        from pickydict import PickyDict

        my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"})
        print(my_dict)  # => {'first name': 'Peter', 'last name': 'Petersson'}

        my_dict.set_pickyness(key_replacements={"last_name": "surname"},
                              key_regex_replacements={r"\\s": "_"})
        print(my_dict)  # => {'first_name': 'Peter', 'surname': 'Petersson'}


    For the rest, PickyDict objects can be used just like regular Python dictionaries!

    """
    _force_lower_case = True
    _key_replacements = None
    _key_regex_replacements = None

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
            An example would be {r"\\s": "_"} which will replace all spaces with underscores.
        force_lower_case : bool, optional
            If set to True (default) all dictionary keys will be forced to be lower case.
        """
        self._force_lower_case = force_lower_case
        self._key_replacements = key_replacements
        self._key_regex_replacements = key_regex_replacements
        if input_dict is not None:
            super().__init__(input_dict)
            self._apply_replacements()
        else:
            super().__init__()     

    def copy(self):
        return PickyDict(self,
                         self._key_replacements,
                         self._key_regex_replacements,
                         self._force_lower_case)

    def __setitem__(self, key, value):
        proper_key = self._harmonize_key(key)
        if key == proper_key:
            super().__setitem__(key, value)
        elif self.get(proper_key, None) is not None:
            raise ValueError(f"Key '{key}' will be interpreted as '{proper_key}'. "
                             "But this entry already exists. "
                             f"Please use '{proper_key}' if you want to replace the entry.")
        else:
            super().__setitem__(proper_key, value)

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
            An example would be {r"\\s": "_"} which will replace all spaces with underscores.
        force_lower_case : bool, optional
            If set to True (default) all dictionary keys will be forced to be lower case.
        """
        self._force_lower_case = force_lower_case
        self._key_replacements = key_replacements
        self._key_regex_replacements = key_regex_replacements
        self._apply_replacements()


    def _harmonize_key(self, key):
        """Applies lower-case, then regex replacements, then key replacements."""
        if self._force_lower_case is True:
            key = key.lower()
        if self._key_regex_replacements is not None:
            for regex_pattern, target in self._key_regex_replacements.items():
                key = re.sub(regex_pattern, target, key)
        if self._key_replacements is not None and key in self._key_replacements:
            key = self._key_replacements[key]
        return key

    def _apply_replacements(self):
        """Harmonizes all keys in dictionary."""
        keys_initial = self.keys()
        for key in list(keys_initial).copy():
            proper_key = self._harmonize_key(key)
            if key != proper_key:
                value = self.get(key)
                if self.get(proper_key) is None:
                    super().__setitem__(proper_key, value)
                elif self.get(proper_key) != value:
                    msg = f"Key '{key}' will be interpreted as '{proper_key}'. " \
                        "But this entry already exists. " \
                        f"Please use '{proper_key}' if you want to replace the entry."
                    logger.warning(msg)
                self.pop(key)

    def to_json(self):
        return json.dumps(self, default=lambda x: x.data, 
            sort_keys=True, indent=4)
    
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
