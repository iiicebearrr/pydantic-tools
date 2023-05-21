# pydantic-tools

[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

A set of tools for pydantic(i18n, alias, etc.)

## i18n

### A simple example

```python
from pydantic_tools import i18n
class TestModel(i18n.BaseModel_i18n):
    name: str
    age: int

    class Config:
        locale = "zh_cn"

test = TestModel()
```

```python
pydantic.error_wrappers.ValidationError: 2 validation errors for TestModel
name
  确保该值不缺失 (type=value_error.missing)
age
  确保该值不缺失 (type=value_error.missing)
```

### Config available

- `locale`: The locale of the model, default is `None`, which means no translation enabled, and the default error message will be used. Use `python -m pydantic_tools.i18n -l` to show all available locales.

- `locale_strict`: Whether to raise an error when the locale is not found, default is `False`.

- `translations`: If specified, the error messages will be translated according to the given dict instead of the locale config. The dict should be like `{"value_error.missing": "Missing"}`. One of `locale` and `translations` should be specified, do not set both of them.

- `extra_translations`: If specified, an extra dict will be merged into the default translations. The dict should be like `{"value_error.missing": "some msg"}`.
