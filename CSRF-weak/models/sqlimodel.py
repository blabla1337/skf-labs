from config.sqlite import * 

class Classes:
    
    def getUser(self, username):
        db = database_con()
        cur = db.execute('SELECT UserId, Username, Password FROM users WHERE Username= ?',
        [username])
        return cur.fetchall()
        
    def getColor(self, userId):
        db = database_con()
        cur = db.execute('SELECT Color FROM prefs WHERE UserId=?',
        [userId])
        return cur.fetchall()
        
    def updateColor(self, color, userId):
        db = database_con()
        cur = db.execute('UPDATE prefs SET Color=? WHERE UserId=?',
        [color, userId])
        db.commit()
        return cur.fetchall()
    
