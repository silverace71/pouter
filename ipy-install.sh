#!/bin/bash

echo "do you wish to intsall pouter (y/n)?"
read confirm
    if [[ $confirm == "y" ]]; then
        sudo apt-get install -y python3 && sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/main.py > pouter.py && sudo python3 pouter.py
    else
        echo "certified bruh moment"
    fi