import typer

from .match import match
from .compare import compare

app = typer.Typer()
app.command()(match)
app.command()(compare)

if __name__ == "__main__":
    app()
