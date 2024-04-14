# daily_commodities_prices
Automated prices data web scraping for rubber from LGM, palm oil from MPOB, crude palm oil futures (FCPO) for current and future from BURSA, cocoa from LKM and Organisation of the Petroleum Exporting Countries (OPEC) Basket Price for each trading day. Script is designed to scrape live data, not historical data.

## Local Project Setup
### Initialisation
1. Create a virtual environment with Python and activate it
2. Download the raw files and save them in the virtual environment folder
   - `requirements.txt`: contains all dependent packages for this project
   - `Daily Commodities Prices.xlsx`: daily historical time series data of 6 commodities to be used to initialise the daily_commodities_prices database provided from 01/03/24 until 01/04/24 (append to dataset manually if you wish the extend the historical data included in your database)
   - `db_init.py`: initialises the daily_commodities_prices database
   - `functions.py`: contains functions to run main.py
   - `classes.py`: contains commodity classes to run main.py
   - `main.py`: main script
   - `db_csv.py`: saves prices table of the daily_commodities_prices into csv
5. Run `pip install -r requirements.txt`
6. Run `db_init.py` to initialise the daily_commodities_prices database
7. Schedule `main.py` to run on your preferred time daily.

## View Database
Run `db_csv.py`

## Note
1. This script hosts prices dataset on SQLite
   - SQLite is a serverless, self-contained, and file-based database management system
   - SQLite is not a cloud-based service. It's a library that you include in your application. The database file resides on your local filesystem or on the filesystem of the machine where your script is running.
   - When your script runs daily and indefinitely, you can use SQLite to store data in a persistent manner between runs. Each time your script runs, it can connect to the SQLite database, perform the scraping, and then store the scraped data in the database. 
2. In case you need to clear your daily_commodities_prices database and re-initialises it, you may run this script:
   ```
   def clear_database(database_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iterate over each table and delete all rows
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name};")

    # Commit changes and close connection
    conn.commit()
    conn.close()

  database_file = 'daily_commodities_prices.db'
  clear_database(database_file)
   ```
