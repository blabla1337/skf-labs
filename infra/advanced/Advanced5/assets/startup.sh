service mysql start 
mysql -u root --password=root -e "CREATE DATABASE SkyTech;"
mysql --password=root --user=root SkyTech < /var/tmp/SkyTech.sql
mysql -u root --password=root -e "CREATE DATABASE Admin;"
mysql --password=root --user=root Admin < /var/tmp/Admin.sql
rm /var/tmp/SkyTech.sql & rm /var/tmp/Admin.sql
#update to native password login 
#https://gist.github.com/rohsyl/e1d459ccd582774e594e3ff3358528d5m
#https://devanswers.co/phpmyadmin-access-denied-for-user-root-localhost/
mysql --password=root --user=root -e "CREATE USER SkyTech@localhost IDENTIFIED BY 'SkyTech';"
mysql --password=root --user=root -e "GRANT SELECT ON mysql.* TO SkyTech@localhost;"
mysql --password=root --user=root -e "GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON SkyTech.* TO SkyTech@localhost;"
mysql --password=root --user=root -e "GRANT CREATE ON Admin.* TO SkyTech@localhost;"
mysql --password=root --user=root -e "UPDATE mysql.user SET authentication_string = PASSWORD('admin12345678') WHERE User = 'root' AND Host = 'localhost';"
mysql --password=root --user=root -e "update mysql.user set plugin = 'mysql_native_password';"
mysql --password=root --user=root -e "SET GLOBAL max_connect_errors = 4294967295;"
mysql --password=root --user=root -e "FLUSH PRIVILEGES;"
service apache2 start
service ssh start 
/bin/sh
