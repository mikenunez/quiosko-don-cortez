#! /bin bash

sudo apt-get update -y
sudo apt-get install -y build-essential libkrb5-dev unzip python3-pip
sudo add-apt-repository ppa:nginx/stable -y
sudo apt-get update -y
y '' | sudo apt-get install -y nginx
## Install Databases
sudo apt-get install -y postgresql postgresql-contrib python-psycopg2 libpq-dev python3-dev
rm /usr/share/quisko-don-cortez.zip
rm -rf /usr/share/quisko-don-cortez
curl -L https://github.com/mikenunez/quiosko-don-cortez/archive/master.zip -o /usr/share/quisko-don-cortez.zip
unzip -uo quisko-don-cortez.zip -d /usr/share/quisko-don-cortez/
exec gunicorn quiosko.wsgi -b 127.0.0.1:8000 --chdir /usr/share/quisko-don-cortez/code
sudo cp -f /usr/share/quiosko-don-cortez/default /etc/nginx/sites-enabled/default
sudo service nginx restart