import typer
import os
import csv
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console

console = Console()
err_console = Console(stderr=True)

def match(
        first_csv: Annotated[Path, typer.Argument(help="Path to the first CSV file")] = None,
        second_csv: Annotated[Path, typer.Argument(help="Path to the second CSV file")] = None,
        fcsv: Annotated[Path | None, typer.Option("-fcsv", "--first-csv", help="Optional flag to specify the first CSV file")] = None,
        scsv: Annotated[Path | None, typer.Option("-scsv", "--second-csv", help="Optional flag to specify the second CSV file")] = None,
        debug: Annotated[bool, typer.Option("-d", "--debug", help="Optional flag to enable debug printing")] = False,
        no_pre_header: Annotated[bool, typer.Option("-nph", "--no-pre-header", help="Optional flag to specify if there is no pre-header in the CSV files")] = False,
        no_header: Annotated[bool, typer.Option("-nh", "--no-header", help="Optional flag to specify if there is no header in the CSV files")] = False,
        no_footer: Annotated[bool, typer.Option("-nf", "--no-footer", help="Optional flag to specify if there is no footer in the CSV files")] = False,
        separator: Annotated[str, typer.Option("-sep", "--separator", help="Optional flag to specify the separator used by the CSV files, default to ','")] = ','
) -> None:
    first_csv = fcsv or first_csv
    second_csv = scsv or second_csv

    if not first_csv or not second_csv \
        or not os.path.isfile(first_csv) or not os.path.isfile(second_csv):
        err_console.print("[bold red]Error: you must provide two CSV files, either positionally or via flags[/bold red]")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Matching `{first_csv}` with `{second_csv}`...[/bold green]")

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
        err_console.print("[bold red]Error: could not match when one of the files is empty[/bold red]")
        raise typer.Exit(code=1)

    if debug:
        console.print(f"First CSV content:\n[yellow]{first_csv_content}[/yellow]")
        console.print(f"Second CSV content:\n[yellow]{second_csv_content}[/yellow]")

