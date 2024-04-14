import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('daily_commodities_prices.db')

# Query the entire contents of the 'prices' table
query = "SELECT * FROM prices"
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Export the DataFrame to a CSV file
data.to_csv('daily_commodities_prices.csv', index=False)

# Print a message indicating that the export is complete
print("Database exported to CSV successfully.")

