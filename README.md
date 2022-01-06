# pickydict
More picky version of Python dictionary


PickyDict objects will behave just like Python dictionaries, with a few
notable exceptions:

(1) PickyDict has a force_lower_case attribute. If set to True (default)
    then dictionary keys will all be treated as lower-case.

(2) PickyDict can contain a second dictionary named "replacements" with
    mappings to enforce translating specific key words.

Examples:


    from pickydict import PickyDict
 
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
