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
print("local files deleted")

for rows in first_batch.itertuples():
    try:
        file_name = f"{rows.url_id}.html"
        pp.get_file(file_name, 'policy_raw')
        pp.convert_html_markdown(rows.url_id)
        pp.markdown_s3_upload(rows.url_id)
        pf.update_doc_id_table(rows.url_id,'convert_markdown')
        dir = Path.cwd()
        uuid_files = dir.glob(f"{rows.url_id}.*")
        for uf in uuid_files:
            uf.unlink()    
    except:
        continue

test = first_batch.iloc[0,0]
file_name = f"{test}.html"
pp.get_file(file_name, 'policy_raw')
pp.convert_html_markdown(test)
pp.markdown_s3_upload(test)


