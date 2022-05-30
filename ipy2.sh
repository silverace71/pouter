#!/bin/bash

sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -t nat -F POSTROUTING
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
sudo echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sudo apt install -y iptables-persistent
sudo iptables-save >/etc/iptables/rules.v4
sudo ip6tables-save >/etc/iptables/rules.v6