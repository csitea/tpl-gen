import os
import pytest
from utils.env_utils import (
    get_env_var,
    get_optional_env_var,
    get_env_as_dict_lower,
    override_env,
)


def test_get_env_var(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "TEST_VALUE")

    assert get_env_var("TEST_VAR") == "TEST_VALUE"

    with pytest.raises(KeyError):
        get_env_var("NON_EXISTING_VAR")


def test_get_optional_env_var(monkeypatch):
    monkeypatch.setenv("TEST_VAR_OPTIONAL", "TEST_VALUE_OPTIONAL")

    assert (
        get_optional_env_var("TEST_VAR_OPTIONAL", "FALLBACK_VALUE")
        == "TEST_VALUE_OPTIONAL"
    )
    assert (
        get_optional_env_var("NON_EXISTING_VAR_OPTIONAL", "FALLBACK_VALUE")
        == "FALLBACK_VALUE"
    )


def test_get_env_as_dict_lower(monkeypatch):
    monkeypatch.setenv("TEST_VAR_LOWERCASE", "TEST_VALUE_LOWERCASE")

    env_dict_lower = get_env_as_dict_lower()

    assert env_dict_lower.get("test_var_lowercase") == "test_value_lowercase"


def test_override_env(monkeypatch):
    cnf = {"env": {"steps": {"001-step-name": {"AWS_PROFILE": "initial_value"}}}}

    monkeypatch.setenv("AWS_PROFILE", "overridden_value")

    cnf_overridden = override_env(cnf)

    assert (
        cnf_overridden["env"]["steps"]["001-step-name"]["AWS_PROFILE"]
        == "overridden_value"
    )
