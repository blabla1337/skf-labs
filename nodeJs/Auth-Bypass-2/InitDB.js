var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");
const crypto = require("crypto");

db.serialize(() => {
  db.run(
    "CREATE TABLE IF NOT EXISTS users(UserId INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, Password TEXT, Hash TEXT)"
  );
  db.run("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?)", [
    1,
    "admin",
    "admin",
    crypto
      .createHash("sha1")
      .update("admin" + "SKFowaspLabs")
      .digest("hex"),
  ]);
});
