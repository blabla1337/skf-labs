mysqldump -u root -p Admin > Admin.sql
openssl enc -aes-256-cbc -salt -in Admin.sql -out backup.enc -k hereisjohn
rm Admin.sql

