#!/bin/bash

systemctl stop squid

script_dir=$(dirname "$0")
stage=$(/opt/hive/bin/python $script_dir/utils/get_stage.py)

cp $script_dir/../.hive/$stage/ca/cacert.pem /etc/squid/bumpcrt.pem
cp $script_dir/../.hive/$stage/ca/cakey.pem /etc/squid/bumpkey.pem
if [ ! -e /etc/squid/bump_dhparam.pem ]; then
  openssl dhparam -outform PEM -out /etc/squid/bump_dhparam.pem 2048
fi
chown proxy:proxy /etc/squid/bump*
chmod 400 /etc/squid/bump*

mkdir -p /var/lib/squid
rm -rf /var/lib/squid/ssl_db
/usr/lib/squid/security_file_certgen -c -s /var/lib/squid/ssl_db -M 20MB
chown -R proxy:proxy /var/lib/squid

systemctl restart squid