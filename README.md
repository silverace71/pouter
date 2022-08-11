# pouter
If you want to have your own network seperate from your main network (this is great for testing), and you want everything to be connected via ethernet, but you don't have any ethernet ports in your house. This is for you

## **HOW DOES IT WORK?**
- it checks for python3
- you configure it
- pi-hole installs (this blocks ads on the network, and it also acts as a dhcpv4 ip giver. Kinda like your router)
- unbound installs(your very own dns so that people cannot track you)
- *magic*
- Reboot the system you are using
---

## **INSTALL POUTER**
```
sudo apt-get install -y python3 && sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/main.py > pouter.py && sudo python3 pouter.py
```
---
## **WARNINGS**
- DO NOT RUN THIS SCRIPT MORE THAN ONCE
- MAKE SURE ```/etc/dhcpcd.conf``` has not been touched before. If you have already configured anything already, please delete anything you added.
---
## ***DEPENDENCIES***
- a problem
- an up to date system with apt package manager on it
- a network switch (optional)
- python (included with the script)
- sudo permisions 
---
### *CREDIT*
- silverace_71 - Getting the problem and tidying up stuff
- ckissane - Actualy doing all of the coding [LINK : https://github.com/ckissane]