from flask import Flask, render_template, request, redirect, url_for, flash
import os
# from Cmpe321-Project3 import routes
# from db import initializeDatabases
import db
import trigger

TYPE = None
FIELD1 = None
FIELD2 = None

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/artist')
def artist():
    global TYPE
    # print(TYPE)
    if(TYPE != 'artist'):
        return render_template('artistlogin.html')
    else:
        return render_template('artist.html')

@app.route('/listener')
def listener():
    if(TYPE != 'listener'):
        return render_template('listenerlogin.html')
    else:
        return render_template('listener.html')

@app.route('/artist', methods=['POST'])
def getCredentialsArtist():
    global TYPE, FIELD1, FIELD2
    if(request and request.method == 'POST'):

        FIELD1 = request.form['name']
        FIELD2 = request.form['surname']
        TYPE = 'artist'
        # print(FIELD1, FIELD2, TYPE)
        return render_template('artist.html')

@app.route('/listener', methods=['POST'])
def getCredentialsListener():
    global TYPE, FIELD1, FIELD2
    FIELD1 = request.form['username']
    FIELD2 = request.form['email']
    TYPE = 'listener'
    # print(FIELD1, FIELD2)
    return render_template('listener.html')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route("/album/add")
def addAlbum():
    return render_template("/album/add.html")

@app.route("/album/add", methods=["POST"])
def postAddAlbum():
    albumid = request.form['id']
    genre = request.form['genre']
    title = request.form['title']
    artistid = f'{FIELD1}~{FIELD2}'
    songs = []
    # print(albumid, genre, title, artistid)
    i=1
    while('songid'+str(i) in request.form):
        songid = request.form['songid'+str(i)]
        songtitle = request.form['songtitle'+str(i)]
        producers = request.form['producers'+str(i)]
        # print(songid, songtitle, producers)
        db.createSong(songid, songtitle, albumid, producers)
        i+=1

    db.createAlbum(albumid, genre, title, FIELD1, FIELD2)
    return redirect(url_for('getCredentialsArtist'))

@app.route('/album/delete')
def deleteAlbum():
    return render_template('/album/delete.html')

@app.route('/album/delete', methods=["POST"])
def postDeleteAlbum():
    albumid = request.form['id']
    ownership = db.ownerAlbumCheck(FIELD1, FIELD2, albumid)
    try:
        if(ownership):
            # print('Correct Owner')
            db.deleteAlbum(albumid)
        else:
            print('You are not authorized for this operation!')
    except:
        print(f'An error while deleting Album {albumid}')
    return redirect(url_for('deleteAlbum'))

@app.route('/album/update')
def updateAlbum():
    return render_template('/album/update.html')

@app.route('/album/update', methods = ["POST"])
def postupdateAlbum():
    albumid = request.form['id']
    title = request.form['title']
    genre = request.form['genre']
    ownership = db.ownerAlbumCheck(FIELD1, FIELD2, albumid)
    try:
        if (ownership):
            print('Correct Owner')
            db.updateAlbum(albumid, title, genre)
        else:
            print('You are not authorized for this operation!')
    except:
        print(f'An error while updating Album {albumid}')
    return redirect(url_for('updateAlbum'))

@app.route('/song/add')
def addSong():
    return render_template('song/add.html') # redirect(url_for('artist'))


@app.route('/song/add', methods = ["POST"])
def postaddsong():
    songid = request.form['id']
    title = request.form['title']
    albumid = request.form['albumid']
    producers = request.form['producers']

    db.addSong(FIELD1, FIELD2, songid, title, albumid, producers)
    return redirect(url_for('addSong'))

@app.route('/song/delete')
def deleteSong():
    return render_template('song/delete.html')

@app.route('/song/delete', methods = ["POST"])
def postdeletesong():
    songid = request.form['id']
    db.deleteSong(FIELD1, FIELD2, songid)
    return redirect(url_for('deleteSong'))


@app.route('/song/update')
def updateSong():
    return render_template('/song/update.html')

@app.route('/song/update', methods = ["POST"])
def postupdateSong():
    songid = request.form['id']
    title = request.form['title']
    producers = request.form['producers']
    db.updateSong(FIELD1, FIELD2, songid, title, producers)
    return redirect(url_for('updateSong'))

@app.route('/song/view')
def viewSongs():
    songs = db.getAllSongs()
    return render_template('/song/view.html',
                            title='Overview',
                            data=songs)

@app.route('/album/view')
def viewAlbums():
    albums = db.getAllAlbums()
    return render_template('/album/view.html',
                            title='Overview',
                            data=albums)

@app.route('/artist/view')
def viewArtists():
    artists = db.getAllArtists()
    # print(artists)
    return render_template('/artist/view.html',
                            title='Overview',
                            data=artists)

@app.route('/artist/info')
def getSongsAlbumsOfArtist():
    # print('getsongsandalbums')
    return render_template('/artist/info.html')

@app.route('/artist/info', methods=['POST'])
def postSongsAlbumsOfArtist():
    # print('postsongsandalbums')
    artistid = request.form['id']
    # print(artistid)
    data = db.songandalbumofartist(artistid)
    # print(data)
    return render_template('/artist/infotable.html',
                            title='Overview',
                            data=data)

@app.route('/album/genre')
def getsongsofagenre():
    # print('getsongsofgenre')
    return render_template('/album/genre.html')


@app.route('/album/genre', methods=['POST'])
def postsongsofagenre():
    # print('postsongsofgenre')
    genre = request.form['genre']
    # print(genre)
    data = db.getSongsOfGenre(genre)
    # print(data)
    return render_template('/album/genretable.html',
                           title='Overview',
                           data=data)

@app.route('/song/search')
def searchSongs():
    # print('searchsongs')
    return render_template('/song/search.html')


@app.route('/song/search', methods=['POST'])
def postsearchSongs():
    # print('postsongsofgenre')
    keyword = request.form['keyword']
    # print(keyword)
    data = db.searchsongs(keyword)
    # print(data)
    return render_template('/song/searchtable.html',
                           title='Overview',
                           data=data)

@app.route('/like/song')
def getlikesongs():
    # print('likesongs')
    data = db.getAllSongs()
    return render_template('/like/song.html',
                            title='Overview',
                            data=data)

@app.route('/like/song', methods = ["POST"])
def postlikesongs():
    # print('likesongs')
    # data = db.getAllSongs()
    songid = request.form['id']
    db.likeSong(FIELD1, songid)
    return redirect(url_for('getlikesongs'))

@app.route('/song/albumsongs')
def getsongsofalbum():
    # print('albumsongs')
    return render_template('/song/albumsongs.html')

@app.route('/song/albumsongs', methods=['POST'])
def postsongsofalbum():
    # print('postalbumsongs')
    albumid = request.form['id']
    # print(albumid)
    data = db.getSongsOfAlbum(albumid)
    # print(data)
    return render_template('/song/albumsongstable.html',
                            title='Overview',
                            data=data)

@app.route('/like/album')
def getlikealbums():
    # print('likealbums')
    data = db.getAllAlbums()
    return render_template('/like/album.html',
                            title='Overview',
                            data=data)

@app.route('/like/album', methods = ["POST"])
def postlikealbums():
    # print('postlikealbums')
    albumid = request.form['id']
    db.likeAlbum(FIELD1, albumid)
    return redirect(url_for('getlikealbums'))


@app.route('/like/viewSongLikes')
def getViewLikedSongs():
    print('view liked songs')
    data = db.viewSongLikes()
    return render_template('/like/viewLikedSongs.html',
                            title='Overview',
                            data=data)

@app.route('/like/viewAlbumLikes')
def getViewLikedAlbums():
    print('view liked albums')
    data = db.viewAlbumLikes()
    return render_template('/like/viewLikedAlbums.html',
                            title='Overview',
                            data=data)

@app.route('/song/viewpopular')
def viewPopularSongs():
    print('view popular songs of an artist')
    return render_template('/song/viewpopular.html')

@app.route('/song/viewpopular', methods= ["POST"])
def postviewPopularSongs():
    print('view popular songs')
    artist = request.form['artist']
    data = db.viewPopularSongs(artist)
    return render_template('/song/viewpopulartable.html',
                           title='Overview',
                           data=data)
@app.route('/artist/rank')
def rankArtist():
    data = db.rankArtists()
    return render_template('/artist/rank.html',
                           title='Overview',
                           data=data)

@app.route('/artist/workedtogether')
def workTogetherArtists():
    return render_template('/artist/workedtogether.html')

@app.route('/artist/workedtogether', methods = ["POST"])
def postworkTogetherArtists():
    artist = request.form['artist']
    data = db.workedTogether(artist)
    # print(data)
    return render_template('/artist/workedtogethertable.html',
                           title='Overview',
                           data=data)

if __name__ == "__main__":
    # db.initializeDatabases()
    # trigger.deleteAlbumTrigger()
    # trigger.likeRemoverTrigger()
    # trigger.likeAlbumTrigger()
    # db.createInitialRecords()
    # db.createStoredProcedure()
    app.run(debug=True, use_reloader=False)
