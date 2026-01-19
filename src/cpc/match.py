import typer
import os
import csv
import collections
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.rule import Rule
from rich.status import Status

console = Console()
err_console = Console(stderr=True)


def match(
        first_csv: Annotated[Path, typer.Argument(help="Path to the first CSV file")] = None,
        second_csv: Annotated[Path, typer.Argument(help="Path to the second CSV file")] = None,
        fcsv: Annotated[Path | None, typer.Option("-fcsv", "--first-csv",
                                                  help="Optional flag to specify the first CSV file")] = None,
        scsv: Annotated[Path | None, typer.Option("-scsv", "--second-csv",
                                                  help="Optional flag to specify the second CSV file")] = None,
        debug: Annotated[bool, typer.Option("-d", "--debug", help="Optional flag to enable debug printing")] = False,
        separator: Annotated[str, typer.Option("-sep", "--separator",
                                               help="Optional flag to specify the separator used by the CSV files, default to ','")] = ','
) -> None:
    console.print(Rule(style="white"))
    first_csv = fcsv or first_csv
    second_csv = scsv or second_csv

    if not first_csv or not second_csv \
            or not os.path.isfile(first_csv) or not os.path.isfile(second_csv):
        err_console.print(
            Panel(
                "[white]Must provide two CSV files, either positionally or via flags[/white]",
                title="Error",
                title_align="left",
                style="red"
            )
        )
        raise typer.Exit(code=1)

    first_csv_content = ""
    second_csv_content = ""
    first_csv_rows = []
    second_csv_rows = []

    with open(first_csv, 'r') as first_csv_file:
        first_csv_reader = csv.reader(first_csv_file, delimiter=separator)
        for row in first_csv_reader:
            first_csv_content += f"{separator}".join(row) + "\n"
            first_csv_rows.append(row)

    with open(second_csv, 'r') as second_csv_file:
        second_csv_reader = csv.reader(second_csv_file, delimiter=separator)
        for row in second_csv_reader:
            second_csv_content += f"{separator}".join(row) + "\n"
            second_csv_rows.append(row)

    if not first_csv_content or not second_csv_content:
        err_console.print(
            Panel(
                "[white]Could not match when one of the files is empty[/white]",
                title="Error",
                title_align="left",
                style="red"
            )
        )
        raise typer.Exit(code=1)

    if debug:
        console.print(
            Panel(
                f"[white]First CSV content:\n{first_csv_content}\n\n" +
                f"Second CSV content:\n{second_csv_content}[/white]",
                title="Debug",
                title_align="left",
                style="yellow"
            )
        )

    matching_status = Status(f"Matching `{first_csv}` with `{second_csv}`")

    match_results = Table(show_lines=True)
    match_results.add_column(f"Row N°({first_csv})", justify="center")
    match_results.add_column("Row text", justify="center")
    match_results.add_column(f"Row N°({second_csv})", justify="center")

    match_counter = 0;
    matching_status.start()
    for i, first_csv_row in enumerate(first_csv_rows):
        for j, second_csv_row in enumerate(second_csv_rows):
            if collections.Counter(first_csv_row) == collections.Counter(second_csv_row):
                match_results.add_row(f"{i}", f"{separator}".join(first_csv_row), f"{j}")
                match_counter += 1
    matching_status.stop()

    console.print(
        Panel(
            Align(
                match_results,
                align="center"
            ),
            title="Matching results",
            title_align="left",
            subtitle=f"[bold green]Found {match_counter} matching rows.[/bold green]"
        )
    )
    console.print(Rule(style="white"))
