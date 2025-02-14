
import os
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, inspect, text

# from sqlalchemy.pool import NullPool

## Prepare data for loading into postgres
raw_import = pd.read_json("town_data_2025-02-13.json")

town_links = raw_import.melt(id_vars=['city'], var_name='policy_type', value_name='source_url')
town_links['source_url'] = town_links['source_url'].str.split(';')
full_list = town_links.explode('source_url')
filtered_df = full_list[full_list['source_url']!='']

# -------------------------------


# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("SUPABASE_KEY")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)


# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

# create raw schema for imports
new_schema = text("""CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION postgres;""")
with engine.connect() as connection:
    connection.execute(new_schema)
    connection.commit()


insp = inspect(engine)
print(insp.get_table_names())

towns = raw_import[['city']]
towns.columns = ['town_name']
towns.head()
towns.to_sql('towns', engine, if_exists='append', index=False)

filtered_df.to_sql("town_links",engine, schema='raw', if_exists='replace')
