import src.postgres_functions as pf
import src.policy_processing as pp
from pathlib import Path

import uuid


first_batch = pf.fetch_rows('ecode')

for rows in first_batch.itertuples():
    try:
        pp.fetch_ecode_file(rows.url_id, rows.source_url)
        pf.update_doc_id_table(rows.url_id,'download_policy')
        pp.raw_s3_upload(rows.url_id, 'ecode')
        pf.update_doc_id_table(rows.url_id,'upload_s3')
    except:
        continue

# Clean local file directory
dir = Path.cwd()
html_files = dir.glob("*.html")
for hf in html_files:
    hf.unlink()


for rows in first_batch.itertuples():
    pass
    
pp.get_file(f"policy_raw\{first_batch.iloc[0,0]}.html")
