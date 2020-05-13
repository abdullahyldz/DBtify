import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123password",
    database="testdb"
)

mycursor = mydb.cursor()


# mycursor.execute("CREATE DATABASE testdb")
# SHOW DATABASES, SHOW TABLES
# mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")

# mycursor.execute()
def createListenersTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS `listeners`")
    mycursor.execute("CREATE TABLE listeners (username VARCHAR(255) NOT NULL PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE)")
    print('listeners table is created.')

def createArtistsTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS `artists`")
    mycursor.execute("CREATE TABLE artists (name VARCHAR(255) NOT NULL, surname VARCHAR(255) NOT NULL)")
    print('artists table is created.')

def createAlbumsTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS `albums`")
    mycursor.execute("CREATE TABLE albums (id INTEGER NOT NULL PRIMARY KEY, genre VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL)")
    print('albums table is created.')

def createSongsTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS `songs`")
    mycursor.execute("CREATE TABLE songs (id INTEGER NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL)")
    print('albums table is created.')


# createListenersTable(mycursor)
# createArtistsTable(mycursor)
# createAlbumsTable(mycursor)
# createSongsTable(mycursor)

