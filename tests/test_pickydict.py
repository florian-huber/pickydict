import json
import os
import pickle
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


def test_pickydict_copy():
    my_dict = PickyDict({"A": 1, "B": 2})
    assert my_dict == {"a": 1, "b": 2}, "Expected different dictionary"

    my_dict_copy = my_dict.copy()
    my_dict_copy["C"] = 3
    assert my_dict_copy.get("c") == 3, "Expected differnt key, value pair"
    assert my_dict.get("c") is None, "Original dictionary should not have changed"


@pytest.mark.parametrize("dict1, dict2, expected", [
    [{"Something": "ABC"}, {"something": "ABC"}, True],
    [{"abc": ["a", 5, 7.01]}, {"abc": ["a", 7.01, 5]}, False],
    [{"abc": 3.7, "def": 4.2}, {"def": 4.2, "abc": 3.7}, True],
    [{"a": 1, "b": 2}, {"b": 2, "a": 1}, True],
    [{"abc": ["a", 5, [7, 1]]}, {"abc":  ["a", 5, [1, 7]]}, False]])
def test_pickydict_equal(dict1, dict2, expected):
    pickydict1 = PickyDict(dict1)
    pickydict2 = PickyDict(dict2)
    if expected is True:
        assert pickydict1 == pickydict2, "Expected dicts to be equal"
    else:
        assert pickydict1 != pickydict2, "Expected dicts NOT to be equal"


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


def test_pickydict_json_dumbs():
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"},
                        key_regex_replacements={r"\s": "_"})
    encoded = json.dumps(my_dict, sort_keys=True)
    expected_encoded = '{"first_name": "Peter", "last_name": "Petersson"}'
    assert encoded == expected_encoded, "Expected differen json.dumbs result"


def test_pickydict_to_json():
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"})
    my_json = my_dict.to_json()
    expected_json = '{\n    "first name": "Peter",\n    "last name": "Petersson"\n}'
    assert my_json == expected_json, "Expected differen json"


def test_pickydict_pickling(tmp_path):
    my_dict = PickyDict({"First Name": "Peter", "Last Name": "Petersson"})
    # Pickling
    file = open(os.path.join(tmp_path, "test.pickle"), "wb")
    pickle.dump(my_dict, file)
    file.close()
    # Un-pickling
    file = open(os.path.join(tmp_path, "test.pickle"), "rb")
    my_dict_unpickled = pickle.load(file)
    file.close()
    assert my_dict == my_dict_unpickled, "Expected equal pickydicts"
