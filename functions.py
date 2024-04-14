from datetime import date, datetime, timedelta

def parse_date(date_str, *formats):
    for format in formats:
        try:
            datetime_obj = datetime.strptime(date_str, format).date()
            return datetime_obj
        except ValueError:
            continue
    return None  # Return None if none of the formats match
    
def format_date(date_obj, format):
    try:
        datetime_str = date_obj.strftime(format)
        return datetime_str
    except ValueError:
        return None
    
def get_date_obj():
    t_0 = date(2024, 4, 10)
    # t_0 = datetime.today().date()
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
    for ele in get_date_obj():
        if ele is not None:
            return ele
    return None