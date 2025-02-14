create or replace view raw.merged_data as
select 
  taba.town_id::uuid ,
  b.source_url,
  b.policy_type
from raw.town_links b
  left join public.towns taba on taba.town_name = b.city 
where b.city is not null;

insert into public.town_policy_urls (town_id, source_url, policy_type)
select * from raw.merged_data;
