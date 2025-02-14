create table public.towns(
    town_id uuid default uuid_generate_v4(),
    town_name text,
    primary key (town_id)
);
comment on table public.towns is 'ID table for towns in Massachusetts';
comment on column public.towns.town_id is 'The town ID';
comment on column public.towns.town_name is "Name of town paired with ID";