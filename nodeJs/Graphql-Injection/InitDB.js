var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./db.sqlite");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, username TEXT, password TEXT, isAdmin INTEGER)"
  );
  // populate users table
  db.run("INSERT OR IGNORE INTO users VALUES(1,'johndoe','password1', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(2,'user','user12312', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(3,'user2','user21234', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(4,'user3','user35466', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(5,'user4','user47547', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(6,'user5','user55745', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(7,'user6','user61239', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(8,'user7','user71112', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(9,'admin','password1337', 1)");
  db.run("INSERT OR IGNORE INTO users VALUES(10,'jimcarry','password88', 1)");
  // create posts table
  db.run(
    "CREATE TABLE IF NOT EXISTS posts ( id INTEGER PRIMARY KEY, title TEXT, body TEXT, author_id INTEGER, FOREIGN KEY(author_id) REFERENCES users(id))"
  );
  // populate posts table
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(1,'Hello World','This is the first post of John', 1)"
  );
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(2,'Woooow','Im the maaaaask', 10)"
  );
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(3,'Second Post John','This is the second post of Jhon', 1)"
  );
  // create user_info table
  db.run(
    "CREATE TABLE IF NOT EXISTS user_info ( id INTEGER PRIMARY KEY , name TEXT, surname TEXT, date_of_birth TEXT, api_key TEXT, user INTEGER)"
  );
  // populate user_info table with 10 different users
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(1,'John','Doe','1990-01-01','klaSKJDOA83847JSDskdjajeb39',1)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(2,'Marc','Zucker','1990-01-01','klajd;aihd9[0jdioha',2)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(3,'Fred','List','1990-01-01','asdkjasd8pu322d8h32d8h2iN',3)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(4,'Jack','Balmore','1990-01-01','PGHJOUKJOK9059069J5J',4)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(5,'Laura','Balmore','1990-01-01','KADSNDCAISDJASIOMAJSIDAJ',5)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(6,'MArta','London','1990-01-01','XCVBCXVBVCXZCVBCX',6)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(7,'Marika','Kovac','1990-01-01','93274146147Y3EUDSBHH',7)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(8,'Alessia','PAnatta','1990-01-01','974YD7ASDAS9DAG79TSAD',8)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(9,'Mika','Hakkinen','1990-01-01','AS7RA968GDBVDQIYILDSY7',9)"
  );
  db.run(
    "INSERT OR IGNORE INTO user_info VALUES(10,'Jim','Carry','1990-01-01','jakshd834oiabvut8bu298bcsiba',10)"
  );
});
