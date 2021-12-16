from config.sqlite import *

class Classes:
    
    def getUser(self, username):
        db = database_con()
        cur = db.execute('SELECT UserId, Username, Password FROM users WHERE Username= ?',
        [username])
        return cur.fetchall()
        
    def CreateUser(self, username,password):
        db = database_con()
        cur = db.cursor()
        cur= cur.execute('insert into users (UserName,Password) VALUES (?,?);',[username,password])
        db.commit()
        return cur.fetchall()
   
    def updatePassword(self, username, password):
        db = database_con()
        cur = db.execute('update users set Password=? where username=?',[password, username])
        db.commit()
        return cur.fetchall()
    
