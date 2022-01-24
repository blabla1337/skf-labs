var sqlite3 = require('sqlite3').verbose();  
var db = new sqlite3.Database('./Database.db3');  


db.serialize(function() {    
    
    db.run("CREATE TABLE IF NOT EXISTS users(UserId INT, UserName TEXT, Password TEXT)");
    db.run("INSERT OR IGNORE INTO users VALUES(1,'Admin','0cef1fb10f60529028a71f58e54ed07b')")
    db.run("INSERT OR IGNORE INTO users VALUES(2,'User','022b5ac7ea72a5ee3bfc6b3eb461f2fc')")
    db.run("INSERT OR IGNORE INTO users VALUES(3,'Guest','94ca112be7fc3f3934c45c6809875168')")
    db.run("INSERT OR IGNORE INTO users VALUES(4,'Plebian','0cbdc7572ff7d07cc6807a5b102a3b93')")

    db.run("CREATE TABLE IF NOT EXISTS pages(pageId INT, title TEXT, content TEXT)")
    db.run("INSERT OR IGNORE INTO pages VALUES(1,'The welcome page','Some text about the welcome page is inserted here')")
    db.run("INSERT OR IGNORE INTO pages VALUES(2,'About','Some text about the about page!')")
    db.run("INSERT OR IGNORE INTO pages VALUES(3,'Contact','Some contact information is found here')")
     
});  
