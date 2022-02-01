var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./db.sqlite");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, username TEXT, isAdmin INTEGER)"
  );
  db.run("INSERT OR IGNORE INTO users VALUES(1,'johndoe', 0)");
  db.run("INSERT OR IGNORE INTO users VALUES(2,'jimcarry', 1)");
  db.run(
    "CREATE TABLE IF NOT EXISTS posts ( id INTEGER PRIMARY KEY, title TEXT, body TEXT, author_id INTEGER)"
  );
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(1,'Hello World','This is the first post of John', 1)"
  );
  db.run("INSERT OR IGNORE INTO posts VALUES(2,'Woooow','Im the maaaaask', 2)");
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(3,'Second Post John','This is the second post of jhon', 1)"
  );
});
