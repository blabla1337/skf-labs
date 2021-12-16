from config.sqlite import * 

class Classes:
    
    def getUser(self, username):
        db = database_con()
        cur = db.execute('SELECT UserId, Username, Password FROM users WHERE Username= ?',
        [username])
        return cur.fetchall()

    def getMessage(self, userId):
        db = database_con()
        cur = db.execute('SELECT Message FROM prefs WHERE UserId=?',
        [userId])
        return cur.fetchall()

    def updateMessage(self, color, userId):
        db = database_con()
        cur = db.execute('UPDATE prefs SET Message=? WHERE UserId=?',
        [color, userId])
        db.commit()
        return cur.fetchall()
    
