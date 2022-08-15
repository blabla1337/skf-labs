from config.sqlite import * 

class DbModel:
    
    def validateUser(self, username, password):
        query = 'SELECT UserId, Username, Password FROM users WHERE Username=\'{}\' AND Password=\'{}\''.format(username, password)
        db = database_con()
        cur = db.execute(query)
        return cur.fetchall()
