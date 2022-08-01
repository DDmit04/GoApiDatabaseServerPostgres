create
user app_user with password 'pswd';

grant all privileges on database
app_db to file_user;

grant all privileges on all
tables in schema public to file_user;

grant all privileges on all
sequences in schema public to file_user;