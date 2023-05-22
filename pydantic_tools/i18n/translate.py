import importlib

TRANSLATIONS = {}


def translate(
    errors: list[dict[str, str | tuple[str]]],
    translations: dict[str, str],
    strict: bool = False,
):
    if strict and not translations:
        raise ValueError("Translations must be provided when strict=True")
    if not translations and not strict:
        return
    for error in errors:
        raw, _type = error["msg"], error["type"]
        if _type in ("type_error", "value_error"):
            continue  # pragma: no cover
        msg = translations.get(_type, raw)
        if strict and msg == raw:
            raise ValueError(f"Translation for {error['type']} not found")
        ctx = error.get("ctx", None)
        if ctx:
            error["msg"] = msg.format(**ctx)
        else:
            error["msg"] = msg


def translate_errors(
    errors: list[dict[str, str | tuple[str]]],
    locale: str = "en_us",
    translations: dict[str, str] | None = None,
    strict: bool = False,
    extra_translations: dict[str, str] | None = None,
):
    if not translations:
        # Get translations by locale
        try:
            translations = TRANSLATIONS[locale]
        except KeyError:
            try:
                module = importlib.import_module(
                    f".locales.{locale}", package=__package__
                )
                translations = getattr(module, "translations", None)
                if translations:
                    TRANSLATIONS[locale] = translations
            except ModuleNotFoundError:
                translations = None

    if extra_translations:
        translations.update(extra_translations)

    translate(errors, translations, strict=strict)
