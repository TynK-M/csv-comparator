import typer
from typing_extensions import Annotated
from pathlib import Path
from rich.console import Console

err_console = Console(stderr=True)

def compare(
        first_csv: Annotated[Path, typer.Argument(help="Path to the first CSV file")] = None,
        second_csv: Annotated[Path, typer.Argument(help="Path to the second CSV file")] = None,
        fcsv: Annotated[Path | None, typer.Option("-fcsv", "--first-csv", help="Optional flag to specify the first CSV file")] = None,
        scsv: Annotated[Path | None, typer.Option("-scsv", "--second-csv", help="Optional flag to specify the second CSV file")] = None
) -> None:
    first_csv = fcsv or first_csv
    second_csv = scsv or second_csv

    if not first_csv or not second_csv:
        err_console.print("[bold red]Error: you must provide two CSV files, either positionally or via flags[/bold red]")
        raise typer.Exit(code=1)

    print(f"Comparing {first_csv} with {second_csv}")

