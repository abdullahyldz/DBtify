# import db
#
# def deleteAlbumTrigger():
#     db.mycursor.execute("DROP TRIGGER IF EXISTS deletealbum")
#     query = 'CREATE trigger deletealbum AFTER DELETE ON albums FOR EACH ROW ' \
#             'DELETE FROM songs WHERE songs.albumid = OLD.id;'
#
#     db.mycursor.execute(query)
#     db.mydb.commit()
#     print('delete album trigger is created', 1)
#
#
# def likeRemoverTrigger():
#     db.mycursor.execute("DROP TRIGGER IF EXISTS likeremover")
#     query = 'create trigger likeremover AFTER DELETE ON songs FOR EACH ROW DELETE FROM likesong WHERE likesong.songid = OLD.id;'
#     db.mycursor.execute(query)
#     db.mydb.commit()
#     print('like remover trigger is created', 1)
#
# def likeAlbumTrigger():
#     db.mycursor.execute("DROP TRIGGER IF EXISTS likealbumtrigger")
#     query = "CREATE trigger likealbumtrigger before insert ON likealbum FOR EACH ROW begin " \
#             "set @albumid = NEW.albumid; set @username = NEW.username; " \
#             "insert ignore into likesong (username, songid) select  @username, id from songs where albumid = @albumid; end;"
#     db.mycursor.execute(query)
#     db.mydb.commit()
#     print('like album trigger is created', 1)