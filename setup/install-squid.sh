#!/bin/bash
script_dir=$(dirname $0)

sudo apt-get -y install squid
sudo cp $script_dir/files/squid.conf /etc/squid/squid.conf
sudo systemctl restart squid
