from tabulate import tabulate

def render_table(
    rows: list[list[str]],
    headers: list[str],
    title: str | None = None,
    footer: str | None = None,
):
    if title:
        print(title)

    print(tabulate(
        rows,
        headers=headers,
        tablefmt="fancy_grid",
        stralign="center",
    ))

    if footer:
        print(footer)
