from config.sqlite import * 

class Classes:
    
    def getUser(self, username):
	    db = database_con()
	    cur = db.execute('SELECT UserId, Username, Password FROM users WHERE Username= ?',
	    [username])
	    return cur.fetchall()
	    
    def getApi(self, userId):
	    db = database_con()
	    cur = db.execute('SELECT API_key FROM prefs_users WHERE UserId=?',
	    [userId])
	    return cur.fetchall()
	    

    
