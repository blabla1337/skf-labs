var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS users(UserId INT, UserName TEXT, Email TEXT, Password TEXT)"
  );
  db.run(
    "INSERT OR IGNORE INTO users VALUES(1,'user', 'user@mail.com' , 'user')"
  );

  db.run(
    "CREATE TABLE IF NOT EXISTS preferences(PreferenceId INT, Color TEXT, UserId INT)"
  );
  db.run("INSERT OR IGNORE INTO preferences VALUES(1,'blue', 1)");
});
