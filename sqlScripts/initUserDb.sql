create schema user_dbs authorization {username};
alter user {username} set search_path = user_dbs;
revoke usage on schema public from {username};