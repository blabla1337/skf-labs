var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");

db.serialize(function () {
  db.run(
    "CREATE TABLE IF NOT EXISTS users(UserId INT, UserName TEXT, Password TEXT)"
  );
  db.run("INSERT OR IGNORE INTO users VALUES(1,'admin','admin')");

  db.run(
    "CREATE TABLE IF NOT EXISTS prefs(PreferenceId INT, Color TEXT, Food TEXT, UserId INT)"
  );
  db.run("INSERT OR IGNORE INTO prefs VALUES(1,'Blue','Apple Pie',1)");
});
