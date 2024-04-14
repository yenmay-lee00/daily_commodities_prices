"""
Author: yenmay
"""
from classes import *
from functions import *

def main():
    global date_obj_1, date_obj_2, date_to_print
    date_obj_1, date_obj_2 = get_date_obj()
    date_to_print = date_to_print()

    commodity_prices = {
        'rubber': Rubber(date_obj_1).get_price(),
        'palm_oil': PalmOil(date_obj_2).get_price(),
        'mdex_current': Mdex(date_obj_1).get_price()[0],
        'mdex_future': Mdex(date_obj_1).get_price()[1],
        'cocoa': Cocoa(date_obj_1).get_price(),
        'OPEC' : OPEC(date_obj_2).get_price()
    }

    print(commodity_prices)

    no_commodity_prices = {
        'rubber': None,
        'palm_oil': None,
        'mdex_current': None,
        'mdex_future': None,
        'cocoa': None,
        'OPEC' : None
    }

    # Establish connection to database
    conn = sqlite3.connect('daily_commodities_prices.db')

    # Find last date in the database
    query = "SELECT MAX(Date) AS max_date FROM prices"
    max_date_df = pd.read_sql_query(query, conn)
    max_date = pd.to_datetime(max_date_df['max_date'].iloc[0])

    # Calculate the date range between max_date and date_to_print
    date_range = pd.date_range(max_date+timedelta(days=1), date_to_print-timedelta(days=1))

    # Convert datetime objects in date_range to date objects
    date_range = [d.date() for d in date_range]

    # Create and insert DataFrame with the date range and NULL values for commodity prices to prices table
    date_range_to_append = pd.DataFrame({'Date': date_range, **no_commodity_prices})
    date_range_to_append.to_sql('prices', conn, if_exists='append', index=False)

    # Create and insert data of the day to prices table
    data_to_append = pd.DataFrame({'Date': [date_to_print], **commodity_prices})
    data_to_append.to_sql('prices', conn, if_exists='append', index=False)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
