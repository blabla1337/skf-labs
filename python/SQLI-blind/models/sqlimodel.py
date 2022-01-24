from config.sqlite import * 

class Pages:
    
    def getPage(self, pageId):
        try:
            db = database_con()
            cur = db.execute('SELECT pageId, title, content FROM pages WHERE pageId='+pageId)
            return cur.fetchone()
        except Exception as e:
            print(e)
            return None
