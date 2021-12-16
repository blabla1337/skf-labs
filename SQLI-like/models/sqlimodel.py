from config.sqlite import * 

class User:
    
    def getUser(self, username):
        db = database_con()
        cur = db.execute("SELECT UserName, email FROM users WHERE UserName LIKE '%"+username+"%' ORDER BY UserId")
        return cur.fetchall()
    
