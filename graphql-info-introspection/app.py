# Imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView




basedir = os.path.abspath(os.path.dirname(__file__))


# app initialization
app = Flask(__name__, static_url_path='/static', static_folder='static')
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

# Schema Objects

class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)
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

@app.route('/')
def index():

    #Implement logic to retrieve posts

    return render_template("index.html",username = "jhon", body="KADJ SDKLASJDKASJ SKDJ S",title="Wow I did not see this" )


if __name__ == '__main__':
     app.run('0.0.0.0')
