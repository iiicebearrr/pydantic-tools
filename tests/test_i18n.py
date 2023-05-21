import pydantic
import pytest

from src import i18n
from src.i18n.locales.zh_cn import translations as translations_zh_cn

_TEST_TRANSLATIONS = translations_zh_cn

_VE = pydantic.ValidationError


def test_missing():
    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale = "zh_cn"
            locale_strict = True

    with pytest.raises(_VE, match=_TEST_TRANSLATIONS["value_error.missing"]):
        TestMissing()


def test_translations():
    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale_strict = True
            translations = {
                "value_error.missing": "Missing value",
            }

    with pytest.raises(_VE, match="Missing value"):
        TestMissing()


def test_extra_trans():
    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale_strict = True
            locale = "zh_cn"
            extra_translations = {
                "value_error.missing": "Missing value Extra",
            }

    with pytest.raises(_VE, match="Missing value Extra"):
        TestMissing()


def test_templates():
    from src.i18n.templates import show_templates

    show_templates()


def test_strict():
    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale_strict = True
            locale = "non-exists"

    with pytest.raises(
        ValueError, match="Translations must be provided when strict=True"
    ):
        TestMissing()

    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale = "non-exists"

    with pytest.raises(_VE):
        TestMissing()

    class TestMissing(i18n.BaseModel_i18n):
        name: str

    with pytest.raises(_VE, match="field required"):
        TestMissing()

    class TestMissing(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale = "zh_cn"
            locale_strict = True
            extra_translations = {
                "value_error.missing": "field required",
            }

    with pytest.raises(
        ValueError, match="Translation for value_error.missing not found"
    ):
        TestMissing()


def test_ctx():
    class TestCtx(i18n.BaseModel_i18n):
        name: str

        class Config:
            locale = "zh_cn"

            min_anystr_length = 10

    with pytest.raises(
        _VE,
        match=_TEST_TRANSLATIONS["value_error.any_str.min_length"].format(
            **{"limit_value": 10}
        ),
    ):
        TestCtx(name="123")
