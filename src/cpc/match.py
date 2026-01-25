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

"""
Declaration of the Rich Console and Error Console.
"""
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
    """
    Show the matching parts of two passed CSV files in the terminal.

    Definition of the CPC command: match.

    :param first_csv: The first CSV path for the comparation
    :param second_csv: The second CSV path for the comparation
    :param fcsv: Optional flag to specify the first CSV path
    :param scsv: Optional flag to specify the second CSV path
    :param debug: A boolean representing if the debug mode is activated or not
    :param separator: The separator used by the CSVs
    """
    console.print(Rule(style="white"))
    first_csv = fcsv or first_csv
    second_csv = scsv or second_csv

    _are_files_provided(first_csv, second_csv)
    _print_info(first_csv=first_csv, second_csv=second_csv, separator=separator, debug=debug)

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

    _are_files_empty(first_csv_content, second_csv_content)
    _print_debug(first_csv_content, second_csv_content, debug)

    _print_result(
        first_csv=first_csv,
        second_csv=second_csv,
        first_csv_rows=first_csv_rows,
        second_csv_rows=second_csv_rows,
        separator=separator
    )
    console.print(Rule(style="white"))


def _are_files_provided(first_csv: str, second_csv: str) -> None:
    """
    Check method to see if there are two passed files, in negative case the command is interrupted and a Rich Panel for the error is shown.

    :param first_csv: The first CSV path for the comparation
    :param second_csv: The second CSV path for the comparation
    """
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


def _are_files_empty(first_csv_content: str, second_csv_content: str) -> None:
    """
    Check method to see if the passed files are empty, in case of an empty file the command is interrupted and a Rich Panel for the error is shown.

    :param first_csv_content: The content of the first CSV file
    :param second_csv_content: The content of the second CSV file
    """
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


def _print_debug(first_csv_content: str, second_csv_content: str, debug: bool = False) -> None:
    """
    Print the debug infos of the matching command as a Rich Panel.

    :param first_csv_content: The content of the first CSV file
    :param second_csv_content: The content of the second CSV file
    :param debug: A boolean representing if the debug mode is activated or not
    """
    if not debug:
        return

    console.print(
        Panel(
            f"[white]First CSV content:\n{first_csv_content.rstrip('\n')}\n\n" +
            f"Second CSV content:\n{second_csv_content.rstrip('\n')}[/white]",
            title="Debug",
            title_align="left",
            style="yellow"
        )
    )


def _print_info(first_csv: str, second_csv: str, separator: str, debug: bool) -> None:
    """
    Print the starting info of the matching command as a Rich Panel.

    :param first_csv: The first CSV path for the comparation
    :param second_csv: The second CSV path for the comparation
    :param separator: The separator used by the CSVs
    :param debug: A boolean representing if the debug mode is activated or not
    """
    info = f"First CSV file: [bold]{first_csv}[/bold]\n" + \
           f"Second CSV file: [bold]{second_csv}[/bold]\n" + \
           f"Separator: [bold]{separator}[/bold]\n" + \
           f"Debug: [bold]{'activated' if debug else 'not activated'}[/bold]"
    console.print(
        Panel(
            info,
            title="Info",
            title_align="left"
        )
    )


def _print_result(first_csv: str, second_csv: str, first_csv_rows: list, second_csv_rows: list, separator: str) -> None:
    """
    Print the results of the matching command as a Rich Panel with inside a Table.

    :param first_csv: The first CSV path for the comparation
    :param second_csv: The second CSV path for the comparation
    :param first_csv_rows: The rows of the first CSV
    :param second_csv_rows: The rows of the second CSV
    :param separator: The separator used by the CSV
    """
    matching_status = Status(f"Matching `{first_csv}` with `{second_csv}`")
    matching_status.start()

    match_results = Table(show_lines=True)
    match_results.add_column(f"Row N°({first_csv})", justify="center")
    match_results.add_column("Row text", justify="center")
    match_results.add_column(f"Row N°({second_csv})", justify="center")

    match_counter = 0;
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
