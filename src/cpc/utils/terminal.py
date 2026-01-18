import shutil

def get_terminal_width() -> int:
    cols, _ = shutil.get_terminal_size()
    return cols

def print_separator(console, separator: str="=") -> None:
    console.print(separator * get_terminal_width())

