from pydantic import BaseModel, ValidationError

from .translate import translate_errors


class BaseModel_i18n(BaseModel):
    def __init__(__pydantic_self__, **data) -> None:
        try:
            super().__init__(**data)
        except ValidationError as ve:
            config = __pydantic_self__.__config__
            locale = getattr(config, "locale", None)
            translations = getattr(config, "translations", None)
            if locale or translations:
                strict = getattr(config, "locale_strict", False)
                extra_translations = getattr(config, "extra_translations", None)
                translate_errors(
                    ve.errors(),
                    locale=locale,
                    translations=translations,
                    strict=strict,
                    extra_translations=extra_translations,
                )
            raise
