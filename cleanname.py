import re

# Define a function to clean up the filenames
def clean_filename(filename):
    # Define regex pattern for substitutions
    pattern = r'[\söüäß|]'
    # Replace matches with their ASCII equivalents or underscores
    filename = re.sub(pattern, lambda x: {' ': '_', 'ö': 'o', 'ü': 'u', 'ä': 'a', 'ß': 'ss', '|': '_'}.get(x.group(0), ''), filename)
    return filename