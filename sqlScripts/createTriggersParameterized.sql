-- {privateSchemaName} - protected schema name
-- {databaseStatsFullTableName} - stats table name with schema
-- {databaseServiceFullTableName} - service table name with schema
create or replace function {privateSchemaName}.update_fill_percent() returns trigger
    security definer
as
$$
begin
    new.fill_percent = ((new.current_bytes)::float / new.max_bytes * 100);
    return new;
end;
$$ language plpgsql;

create trigger on_sizes_update
    before update
    on {databaseStatsFullTableName}
    for each row
    when (new.current_bytes <> old.current_bytes)
execute function {privateSchemaName}.update_fill_percent();


create or replace function {privateSchemaName}.check_max_size() returns trigger
    security definer
as
$$
begin
    if new.max_bytes < new.current_bytes then
        raise exception 'New max db size less than current db size! New max data size = %, old max data size = %, Current data size = %. Try "vacuum full", delete some data or upgrade your db tariff',
            pg_size_pretty(cast(new.max_size as numeric)), pg_size_pretty(cast(old.max_size as numeric)), pg_size_pretty(cast(new.current_size as numeric));
    end if;
    return new;
end;
$$ language plpgsql;

create trigger on_max_size_update
    before update
    on {databaseStatsFullTableName}
    for each row
    when (new.max_bytes <> old.max_bytes)
execute function {privateSchemaName}.update_fill_percent();


create or replace function {privateSchemaName}.on_data_changed() returns trigger
    security definer
as
$$
declare
    new_size bigint = 0;
begin
    select * into new_size from {privateSchemaName}.calc_user_schemas_size();
    update {databaseStatsFullTableName} set current_bytes = new_size where one_id = true;
    call {privateSchemaName}.test_fill_percent();
    return new;
end;
$$ language plpgsql;

create or replace function {privateSchemaName}.on_data_deleted() returns trigger
    security definer
as
$$
declare
    new_size bigint = 0;
begin
    select * into new_size from {privateSchemaName}.calc_user_schemas_size();
    update {databaseStatsFullTableName} set current_bytes = new_size;
end;
$$ language plpgsql;


create or replace procedure {privateSchemaName}.test_fill_percent()
    security definer
as
$$
declare
    current_fill_percent float;
    current_size         int;
    max_size             int;
begin
    select fill_percent into current_fill_percent from {databaseStatsFullTableName};
    select current_bytes into current_size from {databaseStatsFullTableName};
    select max_bytes into max_size from {databaseStatsFullTableName};
    if current_fill_percent > 100.0 then
        raise exception 'Too many memory usage! Max data size = %, Current data size = %. Try "vacuum full", delete some data or upgrade your db tariff',
            pg_size_pretty(cast(max_size as numeric)), pg_size_pretty(cast(current_size as numeric));
    end if;
end;
$$ language plpgsql;

create or replace function {privateSchemaName}.calc_user_schemas_size() returns bigint
    security definer as
$$
declare
    schema_size bigint = 0;
    res_size    bigint = 0;
begin
    select * into schema_size from {privateSchemaName}.pg_schema_size('public');
    res_size = res_size + schema_size;
    return res_size;
end;
$$ language plpgsql;

create or replace function {privateSchemaName}.pg_schema_size(schema_name varchar) returns bigint
    security definer
as
$$
select sum(pg_total_relation_size(quote_ident(schemaname) || '.' || quote_ident(tablename)))::bigint
from pg_tables
where schemaname = quote_ident(schema_name)
$$ language sql;


create or replace function {privateSchemaName}.gen_trigger_name() returns varchar
    security definer
as
$$
declare
    res varchar;
begin
    select into res array_to_string(array((select substring('abcdefghjklmnpqrstuvwxyz'
                                                            from mod((random() * 32)::int, 32) + 1 for 1)
                                           from generate_series(1, 10))), '');
    return res;
end;
$$ language plpgsql;

create or replace function {privateSchemaName}.setup_table_triggers() returns event_trigger
    security definer
    language plpgsql as
$$
declare
    table_name          varchar;
    insert_trigger_name varchar;
    delete_trigger_name varchar;
    update_trigger_name varchar;
    r                   record;
begin
    for r in select * from pg_event_trigger_ddl_commands()
        loop
            if r.command_tag = 'CREATE TABLE' then
                table_name = r.object_identity;
                select * into insert_trigger_name from {privateSchemaName}.gen_trigger_name();
                select * into delete_trigger_name from {privateSchemaName}.gen_trigger_name();
                select * into update_trigger_name from {privateSchemaName}.gen_trigger_name();
--                 TODO add trigger for index create
                execute ('create trigger ' || insert_trigger_name || ' before insert on ' || table_name ||
                         ' execute function {privateSchemaName}.on_data_changed();');
                
                execute ('create trigger ' || delete_trigger_name || ' before delete on ' || table_name ||
                         ' execute function {privateSchemaName}.on_data_deleted();');
                
                execute ('create trigger ' || update_trigger_name || ' before update on ' || table_name ||
                         ' execute function {privateSchemaName}.on_data_changed();');
                insert into {databaseServiceFullTableName}(table_id, trigger_names)
                values (table_name, array [insert_trigger_name, delete_trigger_name, update_trigger_name]);
            end if;
        end loop;
end ;
$$;

create event trigger setup_table_trigger on ddl_command_end
    when tag in ('CREATE TABLE')
execute function {privateSchemaName}.setup_table_triggers();

create or replace function {privateSchemaName}.deny_trigger_delete() returns event_trigger
    security definer
as
$$
declare
    trigger_name      varchar;
    is_system_trigger bool;
begin
    select object_identity into trigger_name from pg_event_trigger_dropped_objects();
    trigger_name = substr(trigger_name, 1, POSITION(' ' IN trigger_name) - 1);
    select exists(select trigger_names
                  from {databaseServiceFullTableName}
                  where quote_ident(trigger_name) = any (trigger_names))
    into is_system_trigger;
    if is_system_trigger then
        raise exception 'you cant delete service trigger!';
    end if;
end ;
$$ language plpgsql;


create event trigger deny_trigger_delete_trigger on sql_drop
    when tag in ('DROP TRIGGER')
execute function {privateSchemaName}.deny_trigger_delete();



create or replace function {privateSchemaName}.on_table_delete() returns event_trigger
    security definer
as
$$
declare
    target_table_id varchar;
begin
    select object_identity into target_table_id from pg_event_trigger_dropped_objects();
    delete from {databaseServiceFullTableName} where table_id = target_table_id;
end;
$$ language plpgsql;

create event trigger table_delete_trigger on sql_drop
    when tag in ('DROP TABLE')
execute function {privateSchemaName}.on_table_delete();
