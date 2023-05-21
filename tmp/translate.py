import traceback
import time
from itertools import chain
from rich import print
from pygoogletranslation import Translator
from src.i18n.locales.templates import get_pydantic_errors_code_templates


def get_langs():
    translator = Translator()
    return translator.glanguage()["tl"]


def translate_locale(locale_code: str):
    translator = Translator()

    def batch_translate(texts: list[str], batch_size: int = 10):
        for i in range(0, len(texts), batch_size):
            results = translator.translate(texts[i : i + batch_size], dest=locale_code)
            for result in results:
                print(
                    f"[light_green bold]\[{locale_code}][/] {result.origin} -> {result.text}"
                )
                yield result.text

    it = list(filter(lambda x: x[1], get_pydantic_errors_code_templates()))

    texts = [template for _, template in it]

    codes = [code for code, _ in it]

    result = list(batch_translate(texts))

    translations = dict(zip(codes, result))

    return translations


def generate_locale(langs: list[str] | None = None):
    langs_valid = get_langs()
    for code in langs:
        name = langs_valid.get(code)
        if not name:
            print(f"[light_red bold]\[ERROR][/] Invalid language code: {code}")
            continue
        print(f"[yellow bold]\[START][/] Translating {code}")
        translations = translate_locale(code)
        # with open(f"src/i18n/locales/{code}.py", "w") as f:
        #     f.write(f"translations = {translations}")
        print(f"[yellow bold]\[END][/] Finished: {code}")

        print(translations)


if __name__ == "__main__":
    langs = [
        "zh-CN",
        "de",
        "fr",
        "ja",
        "ko",
        "ru",
    ]
    generate_locale(["zh-CN"])
