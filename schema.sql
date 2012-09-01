-- This is my `pg_dump -s points` edited to be more compact.
-- When I created this table in 2007, it didn't occur to me that "time"
-- was a reserved word, but it's never caused me any trouble. Thostgres.

create table points (
    "time" timestamp with time zone primary key,
    lat double precision,
    lon double precision,
    ele double precision,
    vel double precision,
    trust boolean default true,
    source text,
    fix text,
    hdop double precision,
    vdop double precision,
    pdop double precision,
    sat integer,
    course double precision
);

create ele_index on points(ele);
create lat_index on points(lat);
create lon_index on points(lon);
create time_index on points("time");
-- And so on. I also have a vdop index at the moment, for example.
alter table points cluster on time_index;
