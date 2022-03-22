service ssh start 
service cron start
crontab -l | { cat; echo "* * * * * /var/backup/backup.sh"; } | crontab -
service mysql start 
mysql -u root -e "CREATE USER 'root'@'%' IDENTIFIED BY 'root';"
mysql -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';"
mysql -u root -e "FLUSH PRIVILEGES;"
mysql -u root --password=root -e "CREATE DATABASE Admin;" 2> /dev/null
mysql --password=root --user=root Admin 2> /dev/null < /var/tmp/Admin.sql 
/bin/sh
