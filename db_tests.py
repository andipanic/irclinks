#!/usr/bin/python

import sqlite3
from os.path import isfile

DATABASE = 'testing.db'
if not isfile(DATABASE):
    created = False
else:
    created = True

def connect(db):
    connection = sqlite3.connect(db)
    if not created:
        cursor = connection.cursor()
        cursor.execute("create table channels ( id primary key not null, name text)")
        cursor.execute("create table urls (nick text, url text, title text, channel_id integer, foreign key (channel_id) references channels(id))")
        connection.commit()

    return connection

def stop(connection):
    connection.commit()
    connection.close()

def make_inserts(connection):
    cursor = connection.cursor()
    cursor.execute("insert into channels values (1, 'cplusplus.com')")
    cursor.execute("insert into urls values ('dont-panic','git.andyblankfield.com','git site',1)")
    connection.commit()

def main():
    connection = connect(DATABASE)
    make_inserts(connection)
    stop(connection)

if __name__ == "__main__":
    main()
