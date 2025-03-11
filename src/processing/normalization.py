import unicodedata
import re

# Define a manual replacement dictionary
replacement_map = {
    "ø": "o",
    "ł": "l",
    "đ": "d",
    "ŋ": "n",
    "ß": "ss",
    "æ": "ae",
    "œ": "oe",
    "ð": "d",
    "þ": "th",
    "ĸ": "k"
}

# Takes first and last names, removes all special and accented characters andand replaces them with their base form.
# Further spaces are replaces by underscores 
def normalize_name(first_name, last_name):
    # Convert None to empty string
    first_name = first_name or ""
    last_name = last_name or ""
    
    # Convert to lowercase
    full_name = f"{first_name} {last_name}".strip().lower()
    
    # Remove accents and special characters
    full_name = ''.join(
        c for c in unicodedata.normalize("NFKD", full_name) if unicodedata.category(c) != "Mn"
    )

    # Normalize to NFKD (splits special characters from accents)
    normalized = unicodedata.normalize("NFKD", full_name)
    
    # Convert accents to base ASCII equivalent
    ascii_text = "".join(c for c in normalized if not unicodedata.combining(c))
    
    # Apply manual replacements for specific cases
    for special_char, replacement in replacement_map.items():
        ascii_text = ascii_text.replace(special_char, replacement)

    # Replace spaces with underscores
    full_name = re.sub(r"\s+", "_", ascii_text)
    
    return full_name