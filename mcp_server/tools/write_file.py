from pathlib import Path 

def read_file(path:str) -> str:
    """
    This function takes text as input and writes it to a file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(text, encoding="utf-8")

    return "Success" # simple way to check things went right