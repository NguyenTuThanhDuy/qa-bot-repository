import re
from functools import wraps

def preprocess_text_decorator(func):
    """
    A decorator that preprocesses the input text before passing it to the actual function.
    It:
    - Converts text to lowercase
    - Removes special characters (except alphanumeric and spaces)
    - Replaces multiple spaces with a single space
    - Strips leading/trailing spaces
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        txt = kwargs.get("input_text")
        # Preprocess the text
        if not isinstance(txt, str):
            raise ValueError("Input must be a string")
        
        # Convert to lowercase
        clean_text = txt.lower()

        # Remove special characters (keep only letters, numbers, and spaces)
        clean_text = re.sub(r"[^a-zA-Z0-9\s]", "", clean_text)

        # Replace multiple spaces with a single space
        clean_text = re.sub(r"\s+", " ", clean_text)

        # Trim leading and trailing spaces
        clean_text = clean_text.strip()

        kwargs["input_text"] = clean_text

        # Call the original function with the cleaned text
        return func(*args, **kwargs)
    
    return wrapper
