DROP TABLE IF EXISTS users;
CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT);
INSERT INTO users VALUES(1,'admin','admin');

DROP TABLE IF EXISTS prefs;
CREATE TABLE prefs(PreferenceId INT, Color TEXT, Food TEXT, UserId INT);
INSERT INTO prefs VALUES(1,'Blue', 'Apple Pie', 1);
