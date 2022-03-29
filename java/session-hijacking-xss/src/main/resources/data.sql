DROP TABLE IF EXISTS users;
CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT);
INSERT INTO users VALUES(1,'admin','admin');

DROP TABLE IF EXISTS prefs;
CREATE TABLE prefs(PreferenceId INT, API_key TEXT, UserId INT);
INSERT INTO prefs VALUES(1,'test', 1);
