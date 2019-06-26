#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import getpass
from mysql.connector import errorcode
from connect import connect


def get_user_home_dir(login, cursor):
    query = ("SELECT home_dir FROM user_atributes WHERE user_login = '{}'".format(login))
    cursor.execute(query)
    result = cursor.fetchall()
    return result[0][0]


def get_user_token(login, cursor):
    query = ("SELECT token FROM user_atributes WHERE user_login = '{}'".format(login))
    cursor.execute(query)
    result = cursor.fetchall()
    return result[0][0]


def list_users(cursor):
    query = ("SELECT user_login FROM user_atributes")
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def take_data(flag):
    result = []
    cnx = connect('root', 'mysqlpassword', 'localhost', 'users_data')
    cursor = cnx.cursor()
    if flag in "get users":
        result = list_users(cursor)
    if flag in "get homedir":
        result = get_user_home_dir("nikitosik", cursor)
    if flag in "get token":
        result = get_user_token("nikitosik", cursor)
    return result


def main():
    data = take_data("get homedir")
    print data

if __name__ == '__main__':
    main()
