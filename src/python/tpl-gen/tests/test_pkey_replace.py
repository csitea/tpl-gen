import pytest
from tpl_gen.lib.utils.string_utils import (
    pkey_replace,
    substring_search,
    extract_pkey_names,
    replace_matching_values,
)

test_values = {"org": "spe", "app": "prp", "env": "dev", "step": "032-some-step"}


@pytest.mark.parametrize(
    "template_path,expected_result",
    [
        ("%org%/%app%/%env%/%step%", "spe/prp/dev/032-some-step"),
    ],
)
def test_pkey_replace(template_path, expected_result):
    assert pkey_replace(template_path, test_values) == expected_result


@pytest.mark.parametrize(
    "template_path,start_index,expected_result,raises",
    [
        ("%org%/%app%/%env%/%step%", 1, ("org", 4), None),
        ("%%", 0, None, KeyError),
    ],
)
def test_substring_search(template_path, start_index, expected_result, raises):
    if raises:
        with pytest.raises(raises):
            substring_search(template_path, start_index)
    else:
        assert substring_search(template_path, start_index) == expected_result


@pytest.mark.parametrize(
    "template_path,expected_result",
    [
        ("%org%/%app%/%env%/%step%", ["org", "app", "env", "step"]),
    ],
)
def test_extract_pkey_names(template_path, expected_result):
    assert extract_pkey_names(template_path) == expected_result


@pytest.mark.parametrize(
    "template_path,keys,expected_result",
    [
        (
            "%org%/%app%/%env%/%step%",
            ["org", "app", "env", "step"],
            "spe/prp/dev/032-some-step",
        ),
    ],
)
def test_replace_matching_values(template_path, keys, expected_result):
    assert replace_matching_values(template_path, keys, test_values) == expected_result
