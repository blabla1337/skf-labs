crontab -l | { cat; echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"; } | crontab -
service cron start 

chmod 777 /usr/share/wordpress/wp-content/themes/twentyseventeen/404.php
service apache2 start 
a2ensite wordpress & a2enmod rewrite & a2dissite 000-default
cp /usr/share/wordpress/wp-config-sample.php /usr/share/wordpress/wp-config.php
service apache2 reload
sed -i 's/database_name_here/wordpress/' /usr/share/wordpress/wp-config.php
sed -i 's/username_here/wordpress/' /usr/share/wordpress/wp-config.php
sed -i 's/password_here/String001/' /usr/share/wordpress/wp-config.php
sed -i 's/localhost/127.0.0.1/' /usr/share/wordpress/wp-config.php
sed -i 's/127.0.0.1/0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf


service vsftpd start
service ssh start
service mysql start 

mysql -u root -e "CREATE DATABASE wordpress;"
mysql -u root -e "CREATE USER wordpress@'%' IDENTIFIED BY 'String001';"
mysql -u root -e "GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON wordpress.* TO wordpress@'%';"
mysql -u root -e "FLUSH PRIVILEGES;"
mysql wordpress < /var/tmp/wordpress.sql
/bin/bash
