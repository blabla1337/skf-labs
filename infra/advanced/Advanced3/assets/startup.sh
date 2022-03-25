service mysql start 
mysql -u root --password=root -e "CREATE DATABASE SkyTech;"
mysql --password=root --user=root SkyTech < /var/tmp/SkyTech.sql
#update to native password login (https://gist.github.com/rohsyl/e1d459ccd582774e594e3ff3358528d5)
# https://devanswers.co/phpmyadmin-access-denied-for-user-root-localhost/
mysql --password=root --user=root  -e "UPDATE mysql.user SET authentication_string = PASSWORD('root') WHERE User = 'root' AND Host = 'localhost';"
mysql --password=root --user=root  -e "update mysql.user set plugin = 'mysql_native_password' where User = 'root';"
mysql --password=root --user=root  -e "SET GLOBAL max_connect_errors = 4294967295;"
mysql --password=root --user=root  -e "FLUSH PRIVILEGES;"
service apache2 start
service ssh start 
/bin/sh
