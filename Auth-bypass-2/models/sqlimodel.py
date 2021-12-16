from config.sqlite import *
import hashlib

class dbaccess:
      
    def getUser(self, username):
        db = database_con()
        cur = db.execute('SELECT Username, Password FROM users WHERE Username= ?',
        [username])
        return cur.fetchall()
        
    def getHash(self, Hash):
        db = database_con()
        cur = db.execute('SELECT Username, Password FROM users WHERE Hash= ?',
        [Hash])
        return cur.fetchall()

    def CreateUser(self, username,password):
        db = database_con()
        #cur = db.cursor()
        cur=db.execute('insert into users (UserName,Password,Hash) VALUES (?,?,?);',[username,password,hashlib.sha1(username.encode('utf-8')+'SKFowaspLabs'.encode('utf-8')).hexdigest()])
        db.commit()
        return cur.fetchall()
   
    def updatePassword(self, username, password):
        db = database_con()
        cur = db.execute('update users set Password=? where username=?',[password, username])
        db.commit()
        return cur.fetchall()
    
