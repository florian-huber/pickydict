from pickydict import PickyDict

def test_pickydict_initialize():
    my_dict = PickyDict({"A": 1, "B": 2})
    assert my_dict == {"a": 1, "b": 2}, "Expected different dictionary"
    assert my_dict._replacemnts is None, "Expected no replacements"




        # now also using a replacements dictionary
        my_dict = PickyDict({"A": 1, "B": 2},
                            replacements={"a": "abc", "b": "bcd", "c": "cde"})
        print(my_dict)  # => {'abc': 1, 'bcd': 2}
        my_dict["c"] = 100
        print(my_dict)  # => {'abc': 1, 'bcd': 2, , 'cde': 100}
    