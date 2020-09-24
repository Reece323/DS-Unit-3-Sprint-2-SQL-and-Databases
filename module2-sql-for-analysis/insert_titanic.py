import os
import json
import sqlite3
import psycopg2
import csv
from psycopg2.extras import execute_values
from psycopg2.extensions import register_adapter, AsIs
from dotenv import load_dotenv
import pandas as pd
import numpy


load_dotenv()

DB_HOST = os.getenv("DB_HOST", default="OOPS")
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module2-sql-for-analysis", "titanic.csv")


connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("-------------------")
print("CONNECTION", type(connection))

cursor = connection.cursor()
print("-------------------")
print("CURSOR", type(cursor))

sql = """
DROP TABLE IF EXISTS passengers;
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived boolean,
    pclass int4,
    full_name text,
    gender text,
    age int4,
    sib_spouse_count int4,
    parent_child_count int4,
    fare float8
);
"""
cursor.execute(sql)

df = pd.read_csv(CSV_FILEPATH)
print("-------------------")
print(df.columns.tolist())
print("-------------------")
print(df.dtypes)
print("-------------------")
print(df.head())

df["Survived"] = df["Survived"].values.astype(bool) # do this before converting to native types, because this actually converts to np.bool
df = df.astype("object") # converts numpy dtypes to native python dtypes (avoids psycopg2.ProgrammingError: can't adapt type 'numpy.int64')

# how to convert dataframe to a list of tuples?
list_of_tuples = list(df.to_records(index=False))


insertion_query = f"INSERT INTO passengers (survived, pclass, full_name, gender, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples) # third param: data as a list of tuples!

# # This block of code is needed so psycopg2 can register numpy types
# def adapt_numpy_float64(numpy_float64):
#     return AsIs(numpy_float64)
# def adapt_numpy_int64(numpy_int64):
#     return AsIs(numpy_int64)
# register_adapter(numpy.float64, adapt_numpy_float64)
# register_adapter(numpy.int64, adapt_numpy_int64)

connection.commit()
cursor.close()
connection.close()
