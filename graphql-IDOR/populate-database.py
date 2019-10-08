from app import db, User, Post, UserInfo
db.create_all()
john = User(username='johndoe', password="password1")
user1 = User(username='user1', password="password10")
user2 = User(username='user2', password="password100")
user3 = User(username='user3', password="password11111111")
user4 = User(username='user4', password="password1231")
user5 = User(username='user5', password="password1444")
user6 = User(username='user6', password="password111")
user7 = User(username='user7', password="password12")
admin = User(username='admin', password="password444555")
john.isAdmin = False
info_john = UserInfo(name="Jhon", surname="Doe", date_of_birth="01/09/1985", api_key="klaSKJDOA83847JSDskdjajeb39",user="1")
info_user1 = UserInfo(name="Marc", surname="Zucker", date_of_birth="01/09/1985", api_key="klajd;aihd9[0jdioha",user="3")
info_user2 = UserInfo(name="Fred", surname="List", date_of_birth="01/08/1983", api_key="asdkjasd8pu322d8h32d8h2iN",user="4")
info_user3 = UserInfo(name="Jack", surname="Balmore", date_of_birth="01/09/1965", api_key="PGHJOUKJOK9059069J5J",user="5")
info_user4 = UserInfo(name="Laura", surname="Fresca", date_of_birth="09/09/1976", api_key="KADSNDCAISDJASIOMAJSIDAJ",user="6")
info_user5 = UserInfo(name="Marta", surname="London", date_of_birth="22/04/1985", api_key="XCVBCXVBVCXZCVBCX",user="7")
info_user6 = UserInfo(name="Marika", surname="Kovac", date_of_birth="17/10/1985", api_key="93274146147Y3EUDSBHH",user="8")
info_user7 = UserInfo(name="Alessia", surname="Panatta", date_of_birth="10/09/1988", api_key="974YD7ASDAS9DAG79TSAD",user="9")
info_admin = UserInfo(name="Mika", surname="Hakkinen", date_of_birth="01/09/1982", api_key="AS7RA968GDBVDQIYILDSY7",user="10")
post = Post()
post.title = "Hello World"
post.body = "This is the first post of jhon"
post.author = john
db.session.add(post)
db.session.add(john)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(user4)
db.session.add(user5)
db.session.add(user6)
db.session.add(user7)
db.session.add(admin)
db.session.add(info_john)
db.session.add(info_user1)
db.session.add(info_user2)
db.session.add(info_user3)
db.session.add(info_user4)
db.session.add(info_user5)
db.session.add(info_user6)
db.session.add(info_user7)
db.session.add(info_admin)

jim = User(username='jimcarry',password="password88")
info_jim = UserInfo(name="Jim", surname="Carry", date_of_birth="22/02/1987",api_key="jakshd834oiabvut8bu298bcsiba",user="2")
jim.isAdmin = True
post2 = Post()
post2.title = "Woooow"
post2.body = "I'm the maaaaask"
post2.author = jim
db.session.add(post2)
db.session.add(jim)
db.session.add(info_jim)
post3 = Post()
post3.title = "Second Post Jhon"
post3.body = "This is the second post of jhon"
post3.author = john
db.session.commit()
