import typer

from .compare import compare

app = typer.Typer()
app.command()(compare)

if __name__ == "__main__":
    app()
