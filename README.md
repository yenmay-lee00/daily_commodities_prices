# daily_commodities_prices
Automated prices data web scraping for rubber from LGM, palm oil from MPOB, crude palm oil futures (FCPO) for current and future from BURSA, cocoa from LKM and Organisation of the Petroleum Exporting Countries (OPEC) Basket Price for each trading day. Script builds time series data based on live data, not historical data.

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
6. Download web driver based on your preferred browser (palm_oil website is built on dynamic HTML, hence selenium was used)
   - [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads)
   - [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads)
   Note: This script uses webdriver.Edge() by default. Please edit code line 56 of `classes.py` if you are using other browsers, e.g. webdriver.Chrome().\
7. Change variables' values in the relevant folder
   - `db_init.py`
      - `file_path`: path where your `Daily Commodities Prices.xlsx` is saved
   - `classes.py`
      - `main_folder_path`: path where daily BURSA files will be temporarily saved
      - `header_general`: your browser header (see how to check [here](https://stackoverflow.com/questions/4423061/how-can-i-view-http-headers-in-google-chrome))
8. Run `db_init.py` to initialise the daily_commodities_prices database
9. Schedule `main.py` to run on your preferred time daily.

## View Database
Run `db_csv.py`

## Note
1. This script hosts prices dataset on SQLite
   - SQLite is a serverless, self-contained, and file-based database management system
   - SQLite is not a cloud-based service. It's a library that you include in your application. The database file resides on your local filesystem or on the filesystem of the machine where your script is running.
   - When your script runs daily and indefinitely, you can use SQLite to store data in a persistent manner between runs. Each time your script runs, it can connect to the SQLite database, perform the scraping, and then store the scraped data in the database. 
2. In case you need to clear your daily_commodities_prices database and re-initialise it, you may run this script:
   ```python
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
## Metadata
### Commodity
| Commodity    | URL                                                                  | URL Time Coverage       | Data Source Type | Data Extraction Rules                                                                                                     | Parent Class | Child Class | date_obj |
|--------------|----------------------------------------------------------------------|-------------------------|------------------|----------------------------------------------------------------------------------------------------------------------------|--------------|-------------|----------|
| rubber       | https://www.lgm.gov.my/webv2api/api/rubberprice/currentprice         | 1 day                   | JSON             | SMR 20 (Sen/Kg)                                                                                                            | Commodity    | Rubber      | date_obj_1 |
| palm_oil     | https://bepi.mpob.gov.my/admin2/chart_cpomsia_mini.php              | 1 day                   | Dynamic HTML     | (RM/TONNE)                                                                                                                 | Commodity    | PalmOil     | date_obj_2 |
| mdex_current | https://www.bursamalaysia.com/market_information/market_statistic/derivatives | 1 month                 | xls              | Tab: "TS_All Prod" tab >> Row Range: FCPO Settlement >> Row: T+0 if date is 1st - 15th; T+1 if date is 16th - EOM       | Commodity    | Mdex        | date_obj_1 |
| mdex_future  | https://www.bursamalaysia.com/market_information/market_statistic/derivatives | 1 month                 | xls              | Tab: "TS_All Prod" tab >> Row Range: FCPO Settlement >> Row: T+2 if date is 1st - 15th; T+3 if date is 16th - EOM       | Commodity    | Mdex        | date_obj_1 |
| cocoa        | https://sso.koko.gov.my/api/carian_HHarian?tarikh={format_date(self.date_obj, '%Y-%m-%d')}&bahasa=English&wpgetapi=[%22api_koko%22,%22carian_harian%22,%22none%22,0] | 1 day (other days accessible via mutating url) | Static HTML      | mean(array of Avg of SMC 2)                                                                                             | Commodity    | Cocoa       | date_obj_1 |
| opec         | opec.org/basket/basketDayArchives.xml                               | 2003-01-02 until most recent | Static HTML | val of BasketList                                                                                                          | Commodity    | OPEC        | date_obj_2 |

### Data Update
| today() | date_obj_1 | date_obj_2 |
|------|---------|------------|
| Mon  | None    | Fri        |
| Tue  | Mon     | Mon        |
| Wed  | Tue     | Tue        |
| Thu  | Wed     | Wed        |
| Fri  | Thu     | Thu        |
| Sat  | Fri     | None       |
| Sun  | None    | None       |
