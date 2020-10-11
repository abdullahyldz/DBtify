# instance/config.py

SECRET_KEY = '69b5f106cf1b4bfab1e3fb65513724cd'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:123password@localhost/testdb'
SQLALCHEMY_DATABASE_URI='mysql+pymysql://{user}:{password}@{server}/{database}'.format(user='root', password='123password', server='localhost', database='testdb')
