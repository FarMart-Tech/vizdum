# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:03:04 2022

@author: nikhil
"""
"""
import pymysql
from pymongo import MongoClient
import pymongo
import psycopg2
"""

"""
SQL_HOST = ""
SQL_USER = ""
SQL_PASSWORD = ""
SQL_DATABASE = ""


def get_sql_connection():
    connection = pymysql.connect(
        host=SQL_HOST,
        user=SQL_USER,
        password=SQL_PASSWORD,
        database=SQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
    )

    return connection


MONGO_USER = ""
MONGO_PASSWORD = ""
MONGO_CONNECTION_STRING = ""


def get_mongo_connection():
    client = MongoClient(MONGO_CONNECTION_STRING)
    return client


POSTGRES_DATABASE = ''
POSTGRES_USER = ''
POSTGRES_PASSWORD = ''
POSTGRES_HOST = ''


def get_postgres_connection():
    conn = psycopg2.connect(database=POSTGRES_DATABASE, user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD, host=POSTGRES_HOST)
    return conn
"""