#!/bin/bash

sudo systemctl restart NetworkManager
sudo nmcli device delete virbr1
sudo nmcli device delete virbr2