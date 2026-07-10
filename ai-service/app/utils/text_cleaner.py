import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Remove HTML tags if present
    text = re.sub(r"<[^>]*>", "", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text
