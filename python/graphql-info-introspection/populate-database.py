from app import db, User, Post
db.create_all()
john = User(username='johndoe')
john.isAdmin = False
post = Post()
post.title = "Hello World"
post.body = "This is the first post of jhon"
post.author = john
db.session.add(post)
db.session.add(john)
jim = User(username='jimcarry')
jim.isAdmin = True
post2 = Post()
post2.title = "Woooow"
post2.body = "I'm the maaaaask"
post2.author = jim
db.session.add(post2)
db.session.add(jim)
post3 = Post()
post3.title = "Second Post Jhon"
post3.body = "This is the second post of jhon"
post3.author = john
db.session.commit()
