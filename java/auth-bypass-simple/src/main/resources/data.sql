DROP TABLE IF EXISTS users;
CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT);
INSERT INTO users VALUES(1,'admin','admin');
INSERT INTO users VALUES(2,'user','user');

DROP TABLE IF EXISTS prefs_users;
CREATE TABLE prefs_users(PreferenceId INT, API_key TEXT, UserId);
INSERT INTO prefs_users VALUES(1,'5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', 1);
INSERT INTO prefs_users VALUES(1,'cbfdac6008f9cab4083784cbd1874f76618d2a97', 2);