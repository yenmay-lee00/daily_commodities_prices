import sqlite3
import pandas as pd

file_path = 'C:/Users/.../Daily Commodities Prices.xlsx' # change to your path to Daily Commodities Prices.xlsx
sheet_name = 'prices'

# Read data from Excel file
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Connect to SQLite database
conn = sqlite3.connect('daily_commodities_prices.db')
cursor = conn.cursor()

# Write data to SQLite database
data.to_sql('prices', conn, if_exists='replace', index=False)

# Update all dates in the database to remove the time component
cursor.execute("UPDATE prices SET Date = DATE(Date);")

# Commit changes and close connection
conn.commit()
conn.close()
