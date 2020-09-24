import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv() #> loads contents of the .env file into the script's environment

# loaded into .env for security 
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

### Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print('CONNECTION', connection)

### A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor()
print('CURSER', cursor)

### An example query
cursor.execute('SELECT * from test_table;')

### Note - nothing happened yet! We need to actually *fetch* from the cursor
result = cursor.fetchall()
print(result)

### in sqlite we can chain execute and fetch ####

# insert data to the table

############################### old way #########################
insert_query = '''
INSERT INTO test_table (name, data) VALUES
(
  'A row name',
  null
),
(
  'Another row, with JSON',
  '{ "a": 1, "b": ["bob", "cat", 42], "c": true }'::JSONB
);
'''

# commit the query 
connection.commit()

# close the cursor
cursor.close()

# close the connection
connection.close()

################################# new way (pass into statment) ###################

my_dict = { "A": 1, "B": ["dog", "cat", 42], "c": 'true' }

# pass in values to query with "cursor exicute"
insert_query = "INSERT INTO test_table (name, data) VALUES (%s, %s)"

cursor.execute(insert_query,
  ('ABC', 'null')
)

cursor.execute(insert_query,
  ('json.dump(my_dict)', json.dumps(my_dict))
)

# commit the query 
connection.commit()

# close the cursor
cursor.close()

# close the connection
# connection.close()

#################################### use function ##################################

# data must be in list of tuples

# my_dict = { "A": '1', "B": ["dog", "cat", '42'], "c": 'true' }

# table_name = 'test_table'

# insertion_query = "INSERT INTO test_table (name, data) VALUES %s"

# psycopg2.extras function
execute_values(cursor, insertion_query, [
  ('A NEW ROW','null'),
  ("another row with json", json.dumps(my_dict)),
  ('test_row_with_functions', '3')
])

#commit the query 
connection.commit()

# close the cursor
cursor.close()

# close the connection
connection.close()

##################### new to psycopg3 #####################
#connection commit
cursor close, connection close#


# print the new 
result = cursor.fetchall()
print(result)