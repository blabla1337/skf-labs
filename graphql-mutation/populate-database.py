from app import db, User, Post
db.create_all()
john = User(username='johndoe')
post = Post()
post.title = "Hello World"
post.body = "This is the first post of jhon"
post.author = john
db.session.add(post)
db.session.add(john)
jim = User(username='jimcarry')
db.session.add(jim)
post2 = Post()
post2.title = "Woooow"
post2.body = "I'm the maaaaask"
post2.author = jim
db.session.add(post2)


db.session.commit()
print(User.query.all())
print(Post.query.all())

