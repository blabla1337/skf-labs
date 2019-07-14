from flask import Flask, render_template, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import base64
import json
import jwt

class User(object):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    
    def __str__(self):
        return f"Welcome {self.username}:{self.role}"

users = [User(1, 'user', 'user','guest'),User(2, 'user2', 'user2','mortal'),User(3,'immortal','immortal','admin')]
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
app.config['SECRET_KEY'] = 'VerylongUnbreakablesecretbecausebruteforceisnotthecase'

jwt2 = JWT(app, authenticate, identity)

@app.route("/")
def start():
    return render_template("index.html")

@app.route('/protected')
def protected():
    token = request.headers['AUTHORIZATION']
    jwt_header,jwt_claims,jwt_signature = token[4:].split(".")
    decoded_jwt_header = base64.b64decode(jwt_header).decode("utf-8", "ignore")
    headers = json.loads(decoded_jwt_header)
    alg = headers['alg']
    if alg=='NONE': 
        claims = jwt.decode(token[4:],verify=False)
    else:
        claims = jwt.decode(token[4:],app.config['SECRET_KEY'],algorithms=[alg])
    userId = claims['identity']
    ret = 'User does not exist'
    for usr in users:
        if usr.id==userId:
            ret = f"Welcome {usr.username}: {usr.role}"
    return ret

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

#curl --header "Content-Type: application/json" --request POST --data '{"username":"admin","password":"admin"}' http://localhost:5000/auth
#curl -i -H "Accept: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDgwOTgxNjEsImlhdCI6MTU0ODA5Nzg2MSwibmJmIjoxNTQ4MDk3ODYxLCJpZGVudGl0eSI6Mn0.vUnhorZy454Iw01WFDsgigu0YpCMzhxx-hPGTuFpwCk" http://localhost:5000/protected
#Null cipher header: eyJ0eXAiOiJKV1QiLCAiYWxnIjoiTk9ORSJ9.