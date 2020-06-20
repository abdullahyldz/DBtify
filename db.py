import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123password",
    database="testdb"
)

mycursor = mydb.cursor()

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
    mycursor.execute("CREATE TABLE albums (id INTEGER NOT NULL PRIMARY KEY, genre VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, artist VARCHAR(255) NOT NULL)")
    print('albums table is created.')

def createSongsTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS `songs`")
    mycursor.execute("CREATE TABLE songs (id INTEGER NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL, albumid VARCHAR(255) NOT NULL, producers VARCHAR(255) NOT NULL)")
    print('songs table is created.')

def createLikeSongTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS likesong")
    mycursor.execute("create table likesong (username varchar(255) NOT NULL , songid INTEGER not null, unique(username, songid))")
    print("likesong table is created.")


def createLikeAlbumTable(mycursor):
    mycursor.execute("DROP TABLE IF EXISTS likealbum")
    mycursor.execute("create table likealbum (username varchar(255) NOT NULL, albumid INTEGER not null, unique(username, albumid))")
    print("likealbum table is created.")


def createAlbum(id, genre, title, field1, field2):
    global mycursor
    query = f"insert into albums VALUES ({id}, '{genre}', '{title}', '{field1}~{field2}')"
    mycursor.execute(query)
    mydb.commit()
    print(f'new album {id} is added')

def createSong(songid1, songtitle1, albumid, producers):
    print('//', songid1, songtitle1, producers)
    global mycursor
    query = f"insert into songs VALUES ({songid1}, '{songtitle1}', '{albumid}', '{producers}')"
    print(query)
    mycursor.execute(query)
    mydb.commit()
    print(f'new songs {songid1} are added')

def ownerAlbumCheck(FIELD1, FIELD2, albumid):
    global mycursor
    query = f"select artist from albums where id = '{albumid}'"
    mycursor.execute(query)
    try:
        owner = mycursor.fetchone()[0]
    except:
        owner = None
    print('owner', owner)
    print(f'{FIELD1}~{FIELD2}', owner, f'{FIELD1}~{FIELD2}'== owner)
    if(f'{FIELD1}~{FIELD2}' == owner):
        return True
    return False

def deleteAlbum(albumid):
    global mycursor
    query = f"delete from albums where id = '{albumid}'"
    mycursor.execute(query)
    mydb.commit()
    print('deleted', albumid)

def updateSong(FIELD1, FIELD2, songid, title, producers):
    global mycursor
    albumid = getAlbumId(songid)
    if (not ownerAlbumCheck(FIELD1, FIELD2, albumid)):
        print('You are not authorized to add song to this album!')
        return
    query = f"update songs set title='{title}', producers = '{producers}' where id = {songid}"
    print(query)
    mycursor.execute(query)
    mydb.commit()

def updateAlbum(albumid, title, genre):
    query = f"update albums set title='{title}', genre = '{genre}' where id = {albumid}"
    print(query)
    mycursor.execute(query)
    mydb.commit()

def getAlbumId(songid):
    global mycursor
    query = f'select albumid from songs where id = {songid}'
    mycursor.execute(query)
    albumid = mycursor.fetchone()[0]
    return albumid

def deleteSong(field1, field2, songid):
    global mycursor
    albumid = getAlbumId(songid)
    if (not ownerAlbumCheck(field1, field2, albumid)):
        print('You are not authorized to add song to this album!')
        return
    query = f"delete from songs where id = '{songid}'"
    mycursor.execute(query)
    mydb.commit()

def addSong(field1, field2, songid, title, albumid, producers):
    global mycursor
    if(not ownerAlbumCheck(field1, field2, albumid)):
        print('You are not authorized to add song to this album!')
        return
    query = f"insert into songs values ({songid}, '{title}', {albumid}, '{producers}')"
    print(query)
    mycursor.execute(query)
    mydb.commit()

def getAllSongs():
    global mycursor
    query = f"select s.*, a.genre, a.title as AlbumTitle, a.artist as Artist from songs s left join albums a on s.albumid = a.id"
    print(query)
    mycursor.execute(query)
    songs = mycursor.fetchall()
    print('songs fetched', songs)
    return songs

def getAllAlbums():
    global mycursor
    query = f"select * from albums"
    print(query)
    mycursor.execute(query)
    albums = mycursor.fetchall()
    print('albums fetched', albums)
    return albums

def getAllArtists():
    global mycursor
    query = f"select * from artists;"
    print(query)
    mycursor.execute(query)
    artists = mycursor.fetchall()
    print('artists fetched', artists)
    return artists


def songandalbumofartist(artistid):
    global mycursor
    query = f"select * from songs s left join albums a on s.albumid = a.id where a.artist = '{artistid}';"
    print(query)
    mycursor.execute(query)
    info = mycursor.fetchall()
    print(f'info about artist {artistid} is fetched', info)
    return info

def getSongsOfGenre(genre):
    global mycursor
    query = f"select * from songs s left join albums a on s.albumid = a.id where a.genre = '{genre}';"
    print(query)
    mycursor.execute(query)
    info = mycursor.fetchall()
    print(f'info about genre {genre} is fetched', info)
    return info

def searchsongs(keyword):
    global mycursor
    query = f"select * from songs where title like '%{keyword}%';"
    print(query)
    mycursor.execute(query)
    info = mycursor.fetchall()
    print(f'song about keyword {keyword} is fetched', info)
    return info


def getSongsOfAlbum(albumid):
    global mycursor
    query = f"select * from songs where albumid= {albumid};"
    print(query)
    mycursor.execute(query)
    info = mycursor.fetchall()
    print(f'song about album id : {albumid} is fetched', info)
    return info

def likeSong(username, songid):
    print('like song ', songid)
    global mycursor
    query = f"insert into likesong values ('{username}', {songid})"
    print(query)
    try:
        mycursor.execute(query)
        mydb.commit()
    except:
        print('An error, duplicate error.')

def likeAlbum(username, albumid):
    print('like album ', albumid)
    global mycursor
    query = f"insert into likealbum values ('{username}', {albumid})"
    print(query)
    try:
        mycursor.execute(query)
        mydb.commit()
    except:
        print('An error, duplicate error.')

def viewSongLikes():
    global mycursor
    query = 'select username, group_concat(songid) from likesong group by username'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

def viewAlbumLikes():
    global mycursor
    query = 'select username, group_concat(albumid) from likealbum group by username'
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

def viewPopularSongs(artist):
    global mycursor
    query = f"select  tmp.id, tmp.title, count(username) as `Likes` from likesong ls " \
            f"right join (" \
            f"select s.id, s.title from songs s left join albums alb on s.albumid = alb.id where alb.artist = '{artist}' " \
            f"or s.producers like '{artist}' or s.producers like concat('%,', '{artist}')" \
            f" or s.producers like concat('{artist}', ',%') or s.producers like concat('%,','{artist}'+',%')) tmp " \
            f"on tmp.id = ls.songid group by songid"
    print(query)
    # return
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

def rankArtists():
    global mycursor
    query = f"select Artist, count(songid) as `Likes` from " \
            f"(select  ls.*, concat(art.name, '~', art.surname) as `artist` from likesong ls " \
            f"left join songs s on s.id = ls.songid " \
            f"left join albums a on a.id = s.albumid " \
            f"right join artists art on concat(art.name, '~', art.surname) = a.artist ) tmp " \
            f"group by artist order by Likes desc"
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

def readInitFile():
    operations = []
    with open('./init.txt', 'r') as f:

        while True:
            # if line is empty
            # end of file is reached
            line = f.readline()
            if not line:
                break
            # Get next line from file
            op = line.split('\n')[0]
            operations.append(op)
    return operations

def createInitialRecords():
    operations = readInitFile()
    global mycursor
    for op in operations:
        mycursor.execute(op)
    mydb.commit()
    print('completed')

def createStoredProcedure():
    global mycursor
    query = "CREATE PROCEDURE workedtogether(IN artistname VARCHAR(255)) BEGIN " \
            "select group_concat(x separator ',') from (select concat(s.producers, ',', a.artist) as x from songs s " \
            "left join albums a on a.id = s.albumid " \
            "where a.artist = artistname or s.producers like concat('%',artistname,'%'))t; END"
    mycursor.execute('drop procedure if exists workedtogether;')
    mycursor.execute(query)
    print('stored procedure is created!')

def helperSplit(data):
    if (data[0]):
        print('data[0]')
        tmp = data[0][0]
        if(tmp):
            print('tmp', tmp)
            data[0] = (','.join(list(set(tmp.split(',')))),)
            print(data, data[0], '!')
    return data


def workedTogether(artist):
    global mycursor
    mycursor.callproc('workedtogether', [artist, ])
    data = [('',)]
    for res in mycursor.stored_results():
        data = res.fetchall()
        if(data):
            data = helperSplit(data)
    return data

def initializeDatabases():
    createListenersTable(mycursor)
    createArtistsTable(mycursor)
    createAlbumsTable(mycursor)
    createSongsTable(mycursor)
    createLikeSongTable(mycursor)
    createLikeAlbumTable(mycursor)

