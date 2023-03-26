#!/bin/bash

echo "do you wish to intsall pouter (y/n)?"
read confirm
	if [[ $confirm == "y" ]]; then
		sudo apt-get update
		sudo apt install dhcpcd5 apt-utils iptables python3 python3-pip unbound -y
		python3 -m pip install requests
		sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/main.py > pouter.py
		sudo python3 pouter.py
	else
		echo "certified bruh moment"
	fi