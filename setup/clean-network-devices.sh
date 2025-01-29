#!/bin/bash

sudo apt-get install -y network-manager
sudo systemctl restart NetworkManager
sudo nmcli device delete virbr1
sudo nmcli device delete virbr2