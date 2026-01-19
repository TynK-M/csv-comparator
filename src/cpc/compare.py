import typer
import os
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.rule import Rule

console = Console()
err_console = Console(stderr=True)


def compare(
        first_csv: Annotated[Path, typer.Argument(help="Path to the first CSV file")] = None,
        second_csv: Annotated[Path, typer.Argument(help="Path to the second CSV file")] = None,
        fcsv: Annotated[Path | None, typer.Option("-fcsv", "--first-csv",
                                                  help="Optional flag to specify the first CSV file")] = None,
        scsv: Annotated[Path | None, typer.Option("-scsv", "--second-csv",
                                                  help="Optional flag to specify the second CSV file")] = None,
        debug: Annotated[bool, typer.Option("-d", "--debug", help="Optional flag to enable debug printing")] = False,
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

    first_csv_content = None
    second_csv_content = None

    with open(first_csv, 'r') as first_csv_file:
        first_csv_content = first_csv_file.read()

    with open(second_csv, 'r') as second_csv_file:
        second_csv_content = second_csv_file.read()

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

    comparing_status = Status(f"Comparing {first_csv} with {second_csv}...")
    comparing_status.start()

    comparing_status.stop()
    console.print(Rule(style="white"))
