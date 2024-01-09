#!/bin/sh
service mysql start;

# Reset MySQL pwd
/usr/bin/mysqladmin -u root -p"root" password "root"

rm -rf file.json;
rm -rf dev/file.json;

sleep 1;

echo "DROP USER IF EXISTS 'hbnb_dev'@'localhost';" | mysql -ulocalhost -uroot -proot;
echo "DROP DATABASE IF EXISTS hbnb_dev_db;" | mysql -ulocalhost -uroot -proot;

sleep 1;

echo "CREATE DATABASE IF NOT EXISTS hbnb_dev_db;" | mysql -ulocalhost -uroot -proot;
echo "CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost';" | mysql -ulocalhost -uroot -proot;
echo "SET PASSWORD FOR 'hbnb_dev'@'localhost' = 'hbnb_dev_pwd';" | mysql -ulocalhost -uroot -proot;
echo "GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';" | mysql -ulocalhost -uroot -proot;
echo "GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';" | mysql -ulocalhost -uroot -proot;
echo "FLUSH PRIVILEGES;" | mysql -ulocalhost -uroot -proot;

sleep 1;

export HBNB_ENV=dev;
export HBNB_MYSQL_USER=hbnb_dev;
export HBNB_MYSQL_PWD=hbnb_dev_pwd;
export HBNB_MYSQL_HOST=localhost;
export HBNB_MYSQL_DB=hbnb_dev_db;
export HBNB_TYPE_STORAGE=db;

echo 'create State name="Arizona"' | ./console.py ;
echo 'create State name="California"' | ./console.py ;
echo 'create State name="Louisiana"' | ./console.py ;
echo 'create State name="Texas"' | ./console.py ;
