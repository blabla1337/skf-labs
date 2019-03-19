from flask import Flask, render_template
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __str__(self):
        return "User(id='%s')" % self.id

users = [User(1, 'admin', 'admin'),User(2, 'user2', 'abcxyz'),]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'

jwt = JWT(app, authenticate, identity)

@app.route("/")
def start():
    return render_template("index.html")

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#curl --header "Content-Type: application/json" --request POST --data '{"username":"admin","password":"admin"}' http://localhost:5000/auth
#curl -i -H "Accept: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDgwOTgxNjEsImlhdCI6MTU0ODA5Nzg2MSwibmJmIjoxNTQ4MDk3ODYxLCJpZGVudGl0eSI6Mn0.vUnhorZy454Iw01WFDsgigu0YpCMzhxx-hPGTuFpwCk" http://localhost:5000/protected
