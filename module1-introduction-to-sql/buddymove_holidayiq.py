import os
import sqlite3
import pandas as pd

df = pd.read_csv('buddymove_holidayiq.csv')
df = df.rename(columns={'User Id': 'User_Id'})
print(f'First rows: {df.head()}')
print(f'Shape: {df.shape}')
print(f'Missing values: \n {df.isnull().sum()}')
print(f'df.describe: \n {df.describe()}')

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "buddymove_holidayiq.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)

cursor = connection.cursor()

df.to_sql('review', con=connection, if_exists='replace')

connection.execute("SELECT * FROM review").fetchall()

#Count how many rows you have - it should be 249!

num_rows = "SELECT COUNT('User_Id') FROM review"

print(f'How many rows: '
      f'{str(cursor.execute(num_rows).fetchall()[0][0])}')

# How many users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category?

nature_shopper_user = "SELECT count('User Id') \
    FROM review \
    WHERE Shopping > 100 \
    AND Nature > 100"

print(f'Nature/Shopper reviewers: '
      f'{str(cursor.execute(nature_shopper_user).fetchall()[0][0])}')
