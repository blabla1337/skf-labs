var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS emptbl (ID INT PRIMARY KEY NOT NULL , UserName TEXT NOT NULL, Password TEXT NOT NULL)"
  );
  db.run("INSERT OR IGNORE INTO emptbl VALUES(1,'admin','admin')");
});
