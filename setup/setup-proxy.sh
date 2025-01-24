#!/bin/bash

sudo apt-get -y install squid
sudo systemctl start squid

hive set http_proxy localhost:3128