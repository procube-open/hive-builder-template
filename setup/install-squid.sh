#!/bin/bash

sudo apt-get -y install squid-openssl
sudo systemctl start squid

/opt/hive/bin/hive set http_proxy localhost:3128