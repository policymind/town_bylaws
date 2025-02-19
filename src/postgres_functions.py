import pandas as pd
from sqlalchemy import text

import tools as tl

PROCESS_COLUMN = {'download_policy':'date_uploaded',
                  'upload_s3': 'date_raw_upload',
                  'convert_markdown':'date_markdowned',
                  'insert_mongo': 'date_mongo_insert'}

engine = tl.get_postgres_engine()

def update_doc_id_table(url_id, process):
    """ update url policy table with date of process completion """

    update_stmt = f"UPDATE public.town_policy_ruls SET {PROCESS_COLUMN[process]} = NOW()::TIMESTAMP  WHERE url_id = {url_id}"

    update_table_qry = text(update_stmt)
    with engine.connect() as connection:
        connection.execute(update_table_qry)
        connection.commit()

def fetch_rows(record_type):
    """ function to update policy id with date of action """
    select_stmt = f"select doc_id, source_url from public.town_policy_ruls WHERE url_type = {record_type}"
    uuid_df = pd.read_sql(select_stmt, engine)

    return uuid_df