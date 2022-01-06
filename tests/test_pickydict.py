from pickydict import PickyDict


def test_pickydict_initialize():
    my_dict = PickyDict({"A": 1, "B": 2})
    assert my_dict == {"a": 1, "b": 2}, "Expected different dictionary"
    assert my_dict._replacements is None, "Expected no replacements"


def test_pickydict_no_lower_case():
    my_dict = PickyDict({"A": 1, "B": 2}, force_lower_case=False)
    assert my_dict == {"A": 1, "B": 2}, "Expected unchanged dictionary"
    assert my_dict._replacements is None, "Expected no replacements"


def test_pickydict_w_replacements():
    my_dict = PickyDict({"A": 1, "B": 2},
                        replacements={"a": "abc", "b": "bcd", "c": "cde"})
    assert my_dict == {'abc': 1, 'bcd': 2}, "Expected different dictionary."
    assert my_dict._replacements == {"a": "abc", "b": "bcd", "c": "cde"}, \
        "Expected other replacements dictionary"

    my_dict["c"] = 100
    assert my_dict == {'abc': 1, 'bcd': 2, 'cde': 100}, \
        "Expected different dictionary."
