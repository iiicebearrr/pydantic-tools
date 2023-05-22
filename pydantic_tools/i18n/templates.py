import inspect

from pydantic import errors


def get_all_templates():
    """Get all templates from pydantic.errors"""

    for name, _cls in inspect.getmembers(errors):
        if (
            inspect.isclass(_cls)
            and issubclass(_cls, errors.PydanticErrorMixin)
            and _cls not in (errors.PydanticErrorMixin,)
            and not name.startswith("_")
        ):
            yield name, _cls


def get_pydantic_errors_code_templates() -> tuple[str, str | None]:
    for _, _cls in get_all_templates():
        code = getattr(_cls, "code", None) or _cls.__name__.replace("Error", "").lower()
        template = getattr(_cls, "msg_template", None)
        base_name = "type_error" if issubclass(_cls, TypeError) else "value_error"

        if base_name in ("type_error", "value_error"):
            yield base_name, template

        yield base_name + "." + code, template


def show_templates():
    from rich import print, table

    def colored(val):
        _color = "bold green" if val else "bold red"
        return f"[{_color}]{val}[/]"

    t = table.Table("Code", "Template", title="Pydantic Errors Group")
    for code, template in get_pydantic_errors_code_templates():
        t.add_row(colored(code), colored(template))
    print(t)
