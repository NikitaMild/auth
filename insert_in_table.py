#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import getpass
from mysql.connector import errorcode
import random
from connect import connect


def GetColumnName(cursor, userdb, usertable):
    get_column_name = ('''SELECT column_name FROM information_schema.columns
                          WHERE table_schema = %s
                          AND table_name = %s ''')
    cursor.execute(get_column_name, (userdb, usertable))
    parameters = cursor.fetchall()
    return parameters


def insertinf(parameters, usertable, cursor, atributes):
    tempstring = "("
    bracket = ")"
    backtick = "`"
    comma = ","
    for parameter in parameters:
        if parameter == parameters[-1]:
            tempstring = tempstring + backtick + parameter[-1] + backtick + bracket
            break;
        tempstring = tempstring + backtick + parameter[0] + backtick + comma

    in_p = ', '.join(['%s'] * len(atributes))
    add_information = ('''INSERT INTO `{0}`
                       {1}
                        VALUES ({2})'''.format(usertable, tempstring, in_p))
    kek = tuple(atributes)
    try:
        cursor.execute(add_information, kek)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            print("Such a table does not exist")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_DATA_TOO_LONG:
            print("Your value is long")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_TRUNCATED_WRONG_VALUE_FOR_FIELD:
            print("Your value is incorrect")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.WARN_DATA_TRUNCATED:
            print("your data is trancated")
            cursor.close()
            cnx.close()
            exit(1)
        elif err.errno == errorcode.ER_DUP_ENTRY:
            print("duplicate entry for key 'PRIMARY'")
            return
        else:
            print(err)
            cursor.close()
            cnx.close()
            exit(1)
    return


def insert_in_table(user_name, user_dir, user_token):
    atributes = [user_name, user_dir, user_token]
    username = "root"
    userpass = "mysqlpassword"
    userhost = "localhost"
    userdb = "users_data"
    usertable = "user_atributes"
    cnx = connect(username, userpass, userhost, userdb)
    cursor = cnx.cursor()
    parameters = GetColumnName(cursor, userdb, usertable)
    insertinf(parameters, usertable, cursor, atributes)
    cnx.commit()
    cursor.close()
    cnx.close()
