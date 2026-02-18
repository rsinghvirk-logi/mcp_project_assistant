from pathlib import Path 

def read_file(path:str) -> str:
    """
    This function reads a text files and returns its contents.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    return file_path.read_text(encoding="utf-8")