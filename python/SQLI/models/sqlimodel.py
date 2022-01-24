from config.sqlite import * 

class Pages:
    
    def getPage(self, pageId):
	    db = database_con()
	    cur = db.execute('SELECT pageId, title, content FROM pages WHERE pageId='+pageId)
	    return cur.fetchall()
    
