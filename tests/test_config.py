import os

import pytest

from pyroll.core import config
from pyroll.core.config import ConfigValue
from enum import Enum


class CustomData:
    def __init__(self, value: int):
        self.value = value

class CustomEnum(Enum):
    A = 1
    B = 2

@config("PYROLL_TEST")
class Config:
    _HIDDEN = True
    hidden = True
    _hidden = True

    VAR = 1
    VAR_FLOAT = 1.1
    VAR_BOOL = True
    VAR_LIST = ["a", "b"]
    VAR_TUPLE = ("a", "b")
    VAR_STR = "abc"
    VAR_DICT = {}
    VAR_ENUM = CustomEnum.A
    PARSED = ConfigValue(CustomData(42), parser=lambda v: CustomData(int(v)))
    SPEC_ENV = ConfigValue(42, env_var="P_SPEC_ENV")


def test_config_default():
    assert Config.VAR == 1


def test_config_env_int(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR", "21")

    assert Config.VAR == 21


def test_config_env_float(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_FLOAT", "3.14")

    assert Config.VAR_FLOAT == 3.14


def test_config_env_bool(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_BOOL", "False")

    assert Config.VAR_BOOL is False


def test_config_env_list(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_LIST", "a,b, c")

    assert Config.VAR_LIST == ["a", "b", "c"]


def test_config_env_tuple(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_TUPLE", "a,b, c")

    assert Config.VAR_TUPLE == ("a", "b", "c")


def test_config_env_dict(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_DICT", "a=1, b=2")

    assert Config.VAR_DICT == {"a": "1", "b": "2"}


def test_config_env_str(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR_STR", "def")

    assert Config.VAR_STR == "def"


@pytest.mark.parametrize("input", ["B", "2"])
def test_config_env_enum(monkeypatch, input):
    monkeypatch.setenv("PYROLL_TEST_VAR_ENUM", input)

    assert Config.VAR_ENUM == CustomEnum.B


def test_config_explicit():
    Config.VAR = 42

    assert Config.VAR == 42


def test_config_env_and_explicit(monkeypatch):
    monkeypatch.setenv("PYROLL_TEST_VAR", "21")
    Config.VAR = 42

    assert Config.VAR == 42


def test_config_hidden():
    assert not hasattr(type(Config), "_HIDDEN")
    assert not hasattr(type(Config), "hidden")
    assert not hasattr(type(Config), "_hidden")


def test_config_del():
    Config.VAR = 42
    assert Config.VAR == 42
    del Config.VAR
    assert Config.VAR == 1


def test_config_meta():
    meta = type(Config)
    assert meta.__name__ == "ConfigMeta"

    assert isinstance(meta.VAR, ConfigValue)


def test_parser(monkeypatch):
    assert Config.PARSED.value == 42
    monkeypatch.setenv("PYROLL_TEST_PARSED", "21")
    assert Config.PARSED.value == 21


def test_env_var_override(monkeypatch):
    assert type(Config).SPEC_ENV.env_var == "P_SPEC_ENV"
    monkeypatch.setenv("P_SPEC_ENV", "21")
    assert Config.SPEC_ENV == 21



