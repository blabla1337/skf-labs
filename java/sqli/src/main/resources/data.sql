DROP TABLE IF EXISTS users;
CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT);
INSERT INTO users VALUES(1,'Admin','0cef1fb10f60529028a71f58e54ed07b');
INSERT INTO users VALUES(2,'User','022b5ac7ea72a5ee3bfc6b3eb461f2fc');
INSERT INTO users VALUES(3,'Guest','94ca112be7fc3f3934c45c6809875168');
INSERT INTO users VALUES(4,'Plebian','0cbdc7572ff7d07cc6807a5b102a3b93');

DROP TABLE IF EXISTS pages;
CREATE TABLE pages(pageId INT, title TEXT, content TEXT);
INSERT INTO pages VALUES(1,'The welcome page','Some text about the welcome page is inserted here');
INSERT INTO pages VALUES(2,'About','Some text about the about page!');
INSERT INTO pages VALUES(3,'Contact','Some contact information is found here');