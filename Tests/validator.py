import pytest
from src.validators import Validator
from pathlib import Path
import yaml


def load_config():
    p = Path(__file__).resolve().parents[1] / 'config.yml'
    with open(p) as f:
        return yaml.safe_load(f)


def test_nric_valid():
    cfg = load_config()
    v = Validator(cfg)
    assert v.validate_nric('S1234567A')[0] is True


def test_nric_invalid():
    cfg = load_config()
    v = Validator(cfg)
    assert v.validate_nric('X1234567A')[0] is False


def test_postal():
    cfg = load_config()
    v = Validator(cfg)
    assert v.validate_postal('123456')[0] is True
    assert v.validate_postal('1234')[0] is False


def test_chargeable():
    cfg = load_config()
    v = Validator(cfg)
    assert v.validate_chargeable_income_calc(100000,20000,80000)[0] is True
    assert v.validate_chargeable_income_calc(100000,15000,90000)[0] is False