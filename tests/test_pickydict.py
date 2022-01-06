import pytest
from pickydict import PickyDict


def test_pickydict_initialize():
    my_dict = PickyDict({"A": 1, "B": 2})
    assert my_dict == {"a": 1, "b": 2}, "Expected different dictionary"
    assert my_dict._key_replacements is None, "Expected no replacements"


def test_pickydict_no_lower_case():
    my_dict = PickyDict({"A": 1, "B": 2}, force_lower_case=False)
    assert my_dict == {"A": 1, "B": 2}, "Expected unchanged dictionary"
    assert my_dict._key_replacements is None, "Expected no replacements"


def test_pickydict_w_key_replacements():
    my_dict = PickyDict({"A": 1, "B": 2},
                        key_replacements={"a": "abc", "b": "bcd", "c": "cde"})
    assert my_dict == {'abc': 1, 'bcd': 2}, "Expected different dictionary."
    assert my_dict._key_replacements == {"a": "abc", "b": "bcd", "c": "cde"}, \
        "Expected other replacements dictionary"

    my_dict["c"] = 100
    assert my_dict == {'abc': 1, 'bcd': 2, 'cde': 100}, \
        "Expected different dictionary."


def test_pickydict_w_key_regex_replacements():
    my_dict = PickyDict({"First Name": "Peter", "Surname": "Petersson"},
                        key_regex_replacements={r"\s": "_"})
    assert my_dict == {'first_name': 'Peter', 'surname': 'Petersson'}, \
        "Expected different dicionary"


def test_pickydict_w_key_and_regex_replacements():
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"},
                        key_replacements={"last_name": "surname"},
                        key_regex_replacements={r"\s": "_"})
    assert my_dict == {'first_name': 'Peter', 'surname': 'Petersson'}, \
        "Expected different dicionary"


@pytest.mark.parametrize("set_key, set_value, get_key",
                         [("A", "test1", "abc"),
                          ("First Name", "testname", "first_name"),
                          ("First Name!", "testname", "first_name"),
                          (",First Name?", "testname", "first_name")])
def test_pickydict_setters_getters(set_key, set_value, get_key):
    my_dict = PickyDict({},
                        key_replacements={"a": "abc", "b": "bcd", "c": "cde"},
                        key_regex_replacements={r"\s": "_",
                                                r"[!?,.]": ""})
    assert my_dict == {}, "Expected empty dictionary."

    my_dict[set_key] = set_value
    assert my_dict[get_key] == set_value, \
        "Expected other key, value pair"


def test_pickydict_set_pickyness_update():
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"})
    assert my_dict == {'first name': 'Peter', 'last name': 'Petersson'}, \
        "Expected different dicionary"
    my_dict.set_pickyness(key_replacements={"last_name": "surname"},
                          key_regex_replacements={r"\s": "_"})
    assert my_dict == {'first_name': 'Peter', 'surname': 'Petersson'}, \
        "Expected different dicionary"


def test_pickydict_replacements_update():
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"},
                        force_lower_case=False)
    assert my_dict == {'First Name': 'Peter', 'Last Name': 'Petersson'}, \
        "Expected different dicionary"
    my_dict.force_lower_case = True
    my_dict.key_replacements = {"last_name": "surname"}
    my_dict.key_regex_replacements = {r"\s": "_"}
    assert my_dict == {'first_name': 'Peter', 'surname': 'Petersson'}, \
        "Expected different dicionary"
