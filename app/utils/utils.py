from datetime import datetime


DEFAULT_DATE_FORMAT = "%Y-%m-%d--%H:%M:%S"


# This function returns the current date in the format DEFAULT_DATE_FORMAT.
def current_date():
    return datetime.now().strftime(DEFAULT_DATE_FORMAT)


# This function tells if a date in string came after another date in string.
# The dates must be in the format DEFAULT_DATE_FORMAT.
def is_date_after(date_1: str, date_2: str):
    return datetime.strptime(date_1, DEFAULT_DATE_FORMAT) > datetime.strptime(date_2, DEFAULT_DATE_FORMAT)
