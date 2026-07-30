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
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if not page_text or not page_text.strip():
                print(f"Skipping empty page {page_number}")
                continue

            pages.append(
                {
                    "page_number" : page_number,
                    "text" : page_text
            }
            )

        return pages
    
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}") from e