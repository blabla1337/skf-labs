from ast import Num
from config.sqlite import *
import sys


class Classes:

    def getUser(self, username):
        db = database_con()
        user = db.execute('SELECT UserId, UserName, Password FROM users WHERE UserName= ?',
        [username])
        return user.fetchall()
	    

    def updateUser(self, password, username):
        db = database_con()
        uuser = db.execute('UPDATE users SET Password=? WHERE username=?',
        [password, username])
        db.commit()
        return uuser.fetchall()


    def newUser(self, username, password):
        db = database_con()
        nu = db.execute('insert into users (UserName, Password) values '\
                 '(?,?)',[username, password])
        db.commit()
        return nu.fetchall()


    def getNotes(self, userId):
        db = database_con()
        sql_select_query = "select Title, Body from notes where userId = " + userId
        cur = db.execute(sql_select_query)
        records = cur.fetchall()
        db.close()
        return records
	    

    def newNote(self, title, body, userId):
        db = database_con()
        nn = db.execute('insert into notes (Title, Body, UserId) values '\
                 '(?,?,?)',[title, body, userId])
        db.commit()
        return nn.fetchall()


    def passwordForget(self, username, resetToken):
        db = database_con()
        cur = db.execute('insert into passwordForget (UserName, ResetToken) values '\
                '(?,?)',[username, resetToken])
        db.commit()
        return cur.fetchall()


    def getToken(self, token):
        db = database_con()
        cur = db.execute('SELECT UserName, ResetToken FROM passwordForget WHERE ResetToken= ?',
	    [token])
        return cur.fetchall()