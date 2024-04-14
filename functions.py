from datetime import date, datetime, timedelta

def parse_date(date_str, *formats):
    """Parse a date string using one of the specified formats.

    Args:
        date_str (str): Date string to parse.
        *formats (str): Date format string(s) to attempt parsing.

    Returns:
        datetime.date or None: Parsed date if successful, else None.
    """
    for format in formats:
        try:
            datetime_obj = datetime.strptime(date_str, format).date()
            return datetime_obj
        except ValueError:
            continue
    return None
    
def format_date(date_obj, format):
    """Format a datetime object into a string using the specified format.

    Args:
        date_obj (datetime): Datetime object to be formatted.
        format (str): Format string to specify the desired output format.

    Returns:
        str or None: Formatted datetime string if successful, else None.
    """
    try:
        datetime_str = date_obj.strftime(format)
        return datetime_str
    except ValueError:
        return None
    
def get_date_obj():
    """Get date objects based on today's date.

    Returns:
        tuple: Two date objects representing specific dates based on today's date, where
        date_obj_1 represents date to extract for rubber, mdex and cocoa
        date_obj_2 represents date to extract for palm_oil and opec.
    """
    t_0 = datetime.today().date()
    t_1 = t_0 - timedelta(1)
    t_3 = t_0 - timedelta(4)

    if t_0.weekday() == 0: # Mon
        date_obj_1 = None
        date_obj_2 = t_3
    elif t_0.weekday() == 5: # Sat
        date_obj_1 = t_1
        date_obj_2 = None
    elif t_0.weekday() == 6: # Sun
        date_obj_1 = None
        date_obj_2 = None
    else:
        date_obj_1 = t_1
        date_obj_2 = t_1

    return date_obj_1, date_obj_2

def date_to_print():
    """Get a single date suitable for printing for the day from the result of get_date_obj.

    Returns:
        datetime.date or None: A date object suitable for printing,
        or None if no suitable date is found.
    """
    for ele in get_date_obj():
        if ele is not None:
            return ele
    return None