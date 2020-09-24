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

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("-------------------")
print("CONNECTION", type(connection))

cursor = connection.cursor()
print("-------------------")
print("CURSOR", type(cursor))


sql_path = "/Users/codyreece/Desktop/DS-Unit-3-Sprint-2-SQL-and-Databases/module1-introduction-to-sql/rpg_db.sqlite3"
lite_conn = sqlite3.connect(sql_path)
lite_cur = lite_conn.cursor()

print("-------------------")
print("Made connections...")

# santiy check part 1
sanity_query = "SELECT COUNT(*) FROM charactercreator_character;"
print("-------------------")
print(f"# Characters in Postgres: {lite_cur.execute(sanity_query).fetchone()[0]}")

# lite_cur.execute("PRAGMA table_info(charactercreator_character);").fetchalll()
# drop table to start from new
drop_character = "DROP TABLE IF EXISTS charactercreator_character;"
cursor.execute(drop_character)
connection.commit()
# create character table
create_character = """
CREATE TABLE charactercreator_character (
    character_id SERIAL PRIMARY KEY,
    name VARCHAR(30),
    level INT,
    exp INT,
    hp INT,
    strength INT,
    intelligence INT,
    dexterity INT,
    wisdom INT
);
"""
cursor.execute(create_character)
connection.commit()
print("-------------------")
print("Created table...")

get_characters = "SELECT * FROM charactercreator_character;"
insert_character = """
INSERT INTO charactercreator_character
(name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES
"""
# get characters from sqlite
rows = lite_cur.execute(get_characters).fetchall()
print("-------------------")
print("Adding characters to postgres db...")
for row in rows:
    # add each row to postgres
    cur_query = insert_character + str(row[1:]) + ";"
    cursor.execute(cur_query)

connection.commit()

# sanity check part 2
cursor.execute(sanity_query)
print("-------------------")
print(f"# Characters in Postgres: {cursor.fetchone()[0]}")
cursor.close()
lite_cur.close()
print("-------------------")
print("Done.")