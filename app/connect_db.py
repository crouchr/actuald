# fixme : note host is localhost
import mysql.connector


def connect_database(hostname, db_name):
    """

    :return:
    """
    print('connect_database() : hostname=' + hostname)
    mydb = mysql.connector.connect(
        host=hostname,
        database=db_name,
        user="metmini",
        password="metmini"
    )

    mycursor = mydb.cursor()

    return (mydb, mycursor)
