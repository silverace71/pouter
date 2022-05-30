# pouter
If you dont have ethernet ports in your house, but you do have wifi, a debian based system, and a network switch. This gives you internet access to the ethernet ports on your switch, and built in ad blocking through pi-hole! (and a subnet).

## **HOW DOES IT WORK?**
- it checks for python3
- you configure it
- pi-hole installs (this also blocks ads network wide!)
- unbound installs
- *magic*
- (OPTIONAL): Reboot the system you are using
---

## **INSTALL POUTER**
```
sudo apt-get install -y python3 && sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/main.py > pouter.py && sudo python3 pouter.py
```
---
## **WARNINGS**
- DO NOT RUN THIS SCRIPT MORE THAN ONCE
- MAKE SURE ```/etc/dhcpcd.conf``` has not been touched before. If you have already configured anything already, please delet anything you added.
---
## ***DEPENDENCIES***
- a problem
- an up to date debian system
- a network switch
- python (included with the script)
- sudo permisions 
---
### *CREDIT*
- silverace_71 - Getting the problem and tidying up stuff
- ckissane - Actualy doing all of the coding [LINK : https://github.com/ckissane]