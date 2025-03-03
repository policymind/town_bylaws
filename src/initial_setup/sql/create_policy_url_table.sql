create table public.town_policy_urls (
  url_id uuid default uuid_generate_v4 () primary key,
  town_id text not null references towns (town_id) INITIALLY DEFERRED,
  source_url TEXT not null,
  policy_type TEXT not null,
  url_type TEXT not null generated always  as (
    case
      when source_url like '%ecode360%' then 'ecode'
      when source_url like '%municode%' then 'municode'
      when source_url like '%.pdf' then 'pdf'
      else 'crawl'
    end) stored,
  created_at timestamp
  date_downloaded timestamp,
  date_raw_upload timestamp,
  date_markdowned timestamp,
  date_mongo_insert timestamp
);

comment on table public.town_policy_urls is 'table of town policy urls scraped from state website';

comment on column public.town_policy_urls.url_id is 'primary key for each policy link';

comment on column public.town_policy_urls.town_id is 'foreign key tied to town name';

comment on column public.town_policy_urls.source_url is 'scraped policy url, can contain multiple!';

comment on column public.town_policy_urls.policy_type is 'policy type: bylaws, zoning, or other';

comment on column public.town_policy_urls.url_type is 'type of link: ecode360, municode, pdf, or further town website. generated.';

comment on column public.town_policy_urls.created_at is 'timestamp of record entry';

comment on column public.town_policy_urls.date_downloaded is 'timestamp of file download from source';

comment on column public.town_policy_urls.date_raw_upload is 'timestamp of file uploaded to s3 in raw format';

comment on column public.town_policy_urls.date_markdowned is 'timestamp of file uploaded to markdown directory reformatted';

comment on column public.town_policy_urls.date_mongo_insert is 'timestamp of md content uploaded into mongodb';