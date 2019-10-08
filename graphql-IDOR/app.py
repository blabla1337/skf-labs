# Imports
from flask import Flask, request,render_template, render_template_string, make_response, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
from flask_httpauth import HTTPBasicAuth



auth = HTTPBasicAuth()

basedir = os.path.abspath(os.path.dirname(__file__))


# app initialization
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "SUPERSECRETKEY"
app.debug = True

# Configs

## Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Modules

## Declaring the database
db = SQLAlchemy(app)

# Models


#     1 User -> N Post 
#
#	  1 Post -> 1 User
#



class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    password = db.Column(db.String(256), index=True, unique=True)
    isAdmin = db.Column(db.Boolean) 
    #posts = db.relationship('Post', backref='users') ## HERE is the problem, that enables to create recursive queries
    posts = db.relationship('Post', backref='author')
    
    def __repr__(self):
        return '<User %r>' % self.username
class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<Post %r>' % self.title

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    surname = db.Column(db.String(256), index=True)
    date_of_birth = db.Column(db.String(256), index=True)
    api_key = db.Column(db.String(256), index=True)
    user = db.Column(db.Integer, db.ForeignKey('users.uuid'))

    def __repr__(self):
        return '<UserInfo %r>' % self.name
    
   
    
    

# Schema Objects

class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       exclude_fields = ('password') #this hides the password in the query for the Users
       filter_fields = {
            'username': ['exact', 'icontains', 'istartswith']
        }
       interfaces = (graphene.relay.Node, )
class UserInfoObject(SQLAlchemyObjectType):
   class Meta:
       model = UserInfo
       filter_fields = ['user']
       interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    #user_info = SQLAlchemyConnectionField(UserInfoObject)
    single_user = graphene.Field(UserInfoObject,user=graphene.Argument(type=graphene.Int,required=True))

    @staticmethod
    def resolve_single_user(args,info,user):
    	query = UserInfoObject.get_query(info=info)
    	if user:
    		query = query.filter(UserInfo.user == user)
    	user_info = query.first()
    	return user_info

schema = graphene.Schema(query=Query)


# Routes

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)


def verify_apikey():
	
	query=db.session.query(UserInfo).filter_by(api_key=request.cookies.get("X-Api-Key"))
	user_info = query.first()
	if user_info:
		
		return user_info
	else:
		return None


@app.route('/')
def index():

	user_info = verify_apikey()
	if  user_info != None:
		user =  user_info.name + " " + user_info.surname 
		return render_template("index.html",username=user)
	else:
		return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
    	
    	username = request.form.get('username')
    	password = request.form.get('password')
    	query = db.session.query(User).filter_by(username=username,password=password)
    	user = query.first()
    	if user:
    		#print(user.uuid)
    		query_api_key = db.session.query(UserInfo).filter_by(user=user.uuid)
    		user_info = query_api_key.first()
    		#print(user_info.api_key)
    		#session["X-Api-Key"] = user_info.api_key
    		response = make_response(redirect('/'))
    		response.set_cookie('X-Api-Key', user_info.api_key)
    		response.set_cookie('uuid', str(user_info.user))

    		
    		return response
    	else:
    		return render_template("login.html",error="username or password are not correct") 
			
		
	
	#    if(password == "admin" or username != "admin"):
    #        return render_template("login.html", error = "invalid username")
    #    if(password != "admin" or username == "admin"):
    #        return render_template("login.html", error = "invalid password for username")
    if request.method == 'GET':
    	return render_template("login.html", error = "")
   
@app.route('/settings')
def settings():

	user_info = verify_apikey()
	if  user_info != None:
		return render_template("settings.html",username=user_info.name)
	else:
		return render_template("login.html")




    


if __name__ == '__main__':
     app.run('0.0.0.0')
