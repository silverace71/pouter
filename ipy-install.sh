#!/bin/bash

echo "do you wish to intsall pouter (y/n)?"
read confirm
    if [[ $confirm == "y" ]]; then
        sudo apt-get update
        sudo apt install apt-utils -y
        sudo apt install iptables
        sudo apt-get install -y python3 && sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/main.py > pouter.py && sudo python3 pouter.py
    else
        echo "certified bruh moment"
    fi