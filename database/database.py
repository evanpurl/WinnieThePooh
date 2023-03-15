import random

from mysql.connector import MySQLConnection, Error
from database.python_mysql_dbconfig import read_db_config


async def gettoken(botname):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"SELECT token from tokens where botname=%(botname)s;"
            user_data = {
                'botname': botname,
            }
            c.execute(sql, user_data)
            role = c.fetchone()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
            return role
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


async def getanswer(question):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            # print('Processing Greeting.')
            c = conn.cursor()
            sql = f"SELECT response from questions where question=%(question)s;"
            user_data = {
                'question': question,
            }
            c.execute(sql, user_data)
            response = c.fetchone()
            if not response:
                return None
            response = response[0].split(", ")
            choice = random.choice(response)
            c.close()
            conn.close()
            return choice
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


async def createserver(server, bot, servername):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"INSERT IGNORE INTO {bot} (serverid, servername) VALUES (%(serverid)s, %(servername)s);"
            user_data = {
                'serverid': server,
                'servername': servername,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e


async def deleteserver(server, bot):
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            c = conn.cursor()

            sql = f"DELETE IGNORE FROM {bot} WHERE serverid = (%(serverid)s);"
            user_data = {
                'serverid': server,
            }
            c.execute(sql, user_data)
            conn.commit()
            c.close()  # Closes Cursor
            conn.close()  # Closes Connection
        else:
            return 'Connection to database failed.'
    except Error as e:
        print(e)
        return e
