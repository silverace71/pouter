# ***pouter***

If you want to have your own network seperate from your main network (this is great for testing), and you want everything to be connected via ethernet, but you don't have any ethernet ports in your house. This is for you. (think wireless ethernet and you get your own network)

## **HOW DOES IT WORK?**

- it installs dependicies
- you follow along and configure it to your liking
- pi-hole installs (this blocks ads on the network, and it also acts as a dhcpv4 ip giver. Kinda like your router)
- unbound installs(your very own dns so that people cannot track you)
- *magic* (you get your own network from it)
- Reboot the system you are using

---

## **INSTALL POUTER**

```sh
wget https://raw.githubusercontent.com/silverace71/pouter/main/ipy-install.sh
```

Then Run

```sh
sudo chmod +x ipy-install.sh
```

Then Run

```sh
./ipy-install.sh
```

---

## **WARNINGS**

- MAKE SURE ```/etc/dhcpcd.conf``` has not been touched before. If you have already configured anything already, please delete anything you added.

---

## ***DEPENDENCIES***

- a wireless and wired connection
- apt

---

## **USE CASES**

- wireless ethernet
- if you hook up a AP (access point) you're able to make you're own wifi (perfect for phones and laptops or computers that are far away)
- ad blocking
- privacy

---

### *CREDIT*

- ckissane - Being good at coding [LINK : https://github.com/ckissane]
- Astro - being the only sensible mf here [LINK : https://astroorbis.com ]
