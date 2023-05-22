import importlib
from pathlib import Path

import click
from bullet import Bullet, colors
from rich import print, table

locale_dir = Path(__file__).parent / "locales"


def list_all_locales():
    for path in locale_dir.glob("*.py"):
        if path.stem == "__init__":
            continue
        module = importlib.import_module(f".locales.{path.stem}", package=__package__)
        translations = getattr(module, "translations", None)
        if translations:
            yield path.stem, translations


locale_trans = dict(list_all_locales())


cli = Bullet(
    prompt="\nPlease choose a locale to show: ",
    choices=list(locale_trans.keys()),
    indent=0,
    align=5,
    margin=2,
    shift=0,
    bullet="●",
    bullet_color=colors.foreground["magenta"],
    word_color=colors.foreground["red"],
    word_on_switch=colors.foreground["green"],
    background_color=colors.background["cyan"],
    background_on_switch=colors.background["yellow"],
    pad_right=5,
)


@click.command()
@click.option("-l", "--list_locales", is_flag=True, help="List available locales")
@click.option("-t", "--show_templates", is_flag=True, help="Show templates")
@click.option(
    "-g",
    "--generate_templates",
    is_flag=True,
    help="Generate locales using translation engine",
)
def main(list_locales: bool, show_templates: bool, generate_templates: bool):
    if show_templates:
        locale_to_show = cli.launch()
        t = table.Table("Code", "Msg template", title=f"Templates for {locale_to_show}")
        for code, msg in locale_trans[locale_to_show].items():
            t.add_row(code, msg)
        print(t)
        exit(0)
    if list_locales:
        for idx, _locale in enumerate(locale_trans):
            print(f"[light_green bold]  {idx + 1}: \[{_locale}]")
        exit(0)

    if generate_templates:
        pass


if __name__ == "__main__":
    main()
