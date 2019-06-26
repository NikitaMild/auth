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


def insertinf(parameters, usertable, check, cursor):
    atributes = []
    for parameter in parameters:
        temp = raw_input("please enter {}: ".format(parameter[0]))
        atributes.append(temp)
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


def run():
    username = "root"
    userpass = "mysqlpassword"
    userhost = "localhost"
    userdb = "users_data"
    usertable = "user_atributes"
    check = []
    cnx = connect(username, userpass, userhost, userdb)
    cursor = cnx.cursor()
    parameters = GetColumnName(cursor, userdb, usertable)
    answer = "yes"
    while answer == "yes":
        insertinf(parameters, usertable, check, cursor)
        cnx.commit()
        answer = raw_input("you still want to enter data? (Yes/No) ").lower()
    cursor.close()
    cnx.close()


def main():
    run()


if __name__ == '__main__':
    main()
