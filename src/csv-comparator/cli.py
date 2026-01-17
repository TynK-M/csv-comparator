import typer

from .match import match

app = typer.Typer()
app.command()(match)

if __name__ == "__main__":
    app()
