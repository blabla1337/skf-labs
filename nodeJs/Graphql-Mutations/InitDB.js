var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./db.sqlite");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, username TEXT)"
  );
  db.run("INSERT OR IGNORE INTO users VALUES(1,'johndoe')");
  db.run("INSERT OR IGNORE INTO users VALUES(2,'jimcarry')");
  db.run(
    "CREATE TABLE IF NOT EXISTS posts ( id INTEGER PRIMARY KEY, title TEXT, body TEXT, author_id INTEGER)"
  );
  db.run(
    "INSERT OR IGNORE INTO posts VALUES(1,'Hello World','This is the first post of John', 1)"
  );
  db.run("INSERT OR IGNORE INTO posts VALUES(2,'Woooow','Im the maaaaask', 2)");
});
