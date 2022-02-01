var sqlite3 = require("sqlite3").verbose();
var db = new sqlite3.Database("./Database.db3");

db.serialize(function () {
  db.run(
    "CREATE TABLE IF NOT EXISTS users(UserId INT, UserName TEXT, Password TEXT, email TEXT)"
  );
  db.run(
    "INSERT OR IGNORE INTO users VALUES(1,'Admin','0cef1fb10f60529028a71f58e54ed07b', 'admin@foobar.com')"
  );
  db.run(
    "INSERT OR IGNORE INTO users VALUES(2,'User','022b5ac7ea72a5ee3bfc6b3eb461f2fc', 'user@lala.com')"
  );
  db.run(
    "INSERT OR IGNORE INTO users VALUES(3,'Guest','94ca112be7fc3f3934c45c6809875168', 'guest@localhost')"
  );
  db.run(
    "INSERT OR IGNORE INTO users VALUES(4,'Plebian','0cbdc7572ff7d07cc6807a5b102a3b93', 'plebian@bla.org')"
  );
});
