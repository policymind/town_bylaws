

import pandas as pd
from sqlalchemy import text

import tools as tl

engine = tl.get_postgres_engine()

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

# -------------------------------
# create raw schema for imports
new_schema = text("""CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION postgres;""")
with engine.connect() as connection:
    connection.execute(new_schema)
    connection.commit()

# -------------------------------
# Prepare data for loading into postgres
raw_import = pd.read_json("town_data_2025-02-13.json")
town_links = raw_import.melt(id_vars=['city'], var_name='policy_type', value_name='source_url')
town_links['source_url'] = town_links['source_url'].str.split(';')
full_list = town_links.explode('source_url')
filtered_df = full_list[full_list['source_url']!='']

# -------------------------------
towns = raw_import[['city']]
towns.columns = ['town_name']
towns.to_sql('towns', engine, if_exists='append', index=False)
filtered_df.to_sql("town_links",engine, schema='raw', if_exists='replace')
