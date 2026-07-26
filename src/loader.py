from pypdf import PdfReader
from pathlib import Path

def extract_text_from_file(path_to_file):
    path = Path(path_to_file)
    if not path.exists():
        raise FileNotFoundError("The path is invalid. Give correct path.")

    if not path.is_file():
        raise ValueError(f"The given path: {path} is not a file.")
    
    if not path.suffix.lower() == ".pdf":
        raise ValueError("Only PDF files are supported")


    try:
        reader = PdfReader(path)
        whole_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text is None:
                continue

            whole_text += page_text + "\n"

        return whole_text
    
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}") from e