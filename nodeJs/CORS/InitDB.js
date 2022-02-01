var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");

db.serialize(function () {
  db.run(
    "CREATE TABLE IF NOT EXISTS users(UserId INT, UserName TEXT, Password TEXT)"
  );
  db.run("INSERT OR IGNORE INTO users VALUES(1,'admin','admin')");

  db.run(
    "CREATE TABLE IF NOT EXISTS pages(PreferenceId INT, Color TEXT, UserId TEXT)"
  );
  db.run("INSERT OR IGNORE INTO pages VALUES(1,'RED','1')");
});
