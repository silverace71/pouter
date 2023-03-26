#!/usr/bin/env python3
import os, subprocess, requests
from getpass import getpass


def test_sudo(pwd=""):
	kwargs = dict(stdout=subprocess.PIPE,encoding="ascii")
	if pwd: kwargs.update(input=pwd)
	return ("OK" in subprocess.run("sudo -S echo OK".split(), **kwargs).stdout)


def get_pi_hole_config(wireless_ipv4_addr,wireless_ipv4_subnet,wired_ipv4_dhcp_start_addr,wired_ipv4_dhcp_end_addr,wired_ipv4_addr,dns,wired_interface,wireless_interface):
	return f"""QUERY_LOGGING=true
PIHOLE_INTERFACE={wireless_interface}
IPV4_ADDRESS={wireless_ipv4_addr}/{wireless_ipv4_subnet}
IPV6_ADDRESS=
QUERY_LOGGING=true
INSTALL_WEB_SERVER=true
INSTALL_WEB_INTERFACE=true
LIGHTTPD_ENABLED=true
CACHE_SIZE=10000
DNS_FQDN_REQUIRED=true
DNS_BOGUS_PRIV=true
DNSMASQ_LISTENING=local
WEBPASSWORD=🐰
BLOCKING_ENABLED=true
ADMIN_EMAIL=
WEBUIBOXEDLAYOUT=boxed
WEBTHEME=default-darker
PIHOLE_DNS_1={dns}
DNSSEC=false
REV_SERVER=false
DHCP_ACTIVE=true
DHCP_START={wired_ipv4_dhcp_start_addr}
DHCP_END={wired_ipv4_dhcp_end_addr}
DHCP_ROUTER={wired_ipv4_addr}
DHCP_LEASETIME=0
PIHOLE_DOMAIN=lan
DHCP_IPv6=false
DHCP_rapid_commit=true
API_EXCLUDE_DOMAINS=
API_EXCLUDE_CLIENTS=
API_QUERY_LOG_SHOW=all
"""

def runnn(stm, pwd=""):
	args = stm.split()
	kwargs = dict(stdout=subprocess.PIPE,
				encoding="ascii")
	pwd=""
	if pwd:
		kwargs.update(input=pwd)
	cmd = subprocess.run(args)

def runnn_bash(stm, pwd=""):
	args = ["bash","-c",stm]
	kwargs = dict(stdout=subprocess.PIPE,
				encoding="ascii")
	pwd=""
	if pwd:
		kwargs.update(input=pwd)
	cmd = subprocess.run(args)


def install_pi_hole(wireless_ipv4_addr, wireless_ipv4_subnet, wired_ipv4_dhcp_start_addr, wired_ipv4_dhcp_end_addr, wired_ipv4_addr, password, wired_interface, wireless_interface):
    conf = get_pi_hole_config(wireless_ipv4_addr, wireless_ipv4_subnet, wired_ipv4_dhcp_start_addr, wired_ipv4_dhcp_end_addr, wired_ipv4_addr, wired_interface, wireless_interface, "1.1.1.1")
    runnn("rm -rf /etc/pihole/setupVars.conf")
    runnn("mkdir -p /etc/pihole/")
    with open("/etc/pihole/setupVars.conf", "w") as f:
        f.write(conf)
    subprocess.run(['sudo', "chmod", "+x", "ipy.sh"])
    subprocess.run(['sudo', 'bash', './ipy.sh'])

    runnn("rm -rf /etc/unbound/unbound.conf.d/pi-hole.conf")
    runnn("mkdir -p /etc/unbound/unbound.conf.d/")
    with open("/etc/unbound/unbound.conf.d/pi-hole.conf", "w") as f:
        f.write(requests.get("https://raw.githubusercontent.com/silverace71/pouter/main/unbound_conf.conf").text)
    runnn(f"sudo ip addr add {wired_ipv4_addr}/24 dev {wired_interface}")



def ask_user_for_interface(p):
	interfaces=[line.split()[0] for line in subprocess.run(["ip","-br","l"],capture_output=True,encoding="utf8").stdout.splitlines()]
	while True:
		try:
			print("Discovered Interfaces:",len(interfaces))
			for i,interface in enumerate(interfaces):
				print("Interface",f'{i:2d}',":",interface)
			interface=interfaces[int(input(p))]
			break
		except:
			print("Invalid interface")
	print("Interface",interface,"selected")
	return interface



if __name__ == '__main__':
	print("Welcome to pouter setup")


	if not (((os.geteuid() == 0) or test_sudo())):
		print("pouter needs sudo privileges to setup")


	print("sudo privileges to setup have been given")
		
	subprocess.run(["sh","-c","sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/ipy.sh > ipy.sh"])
	subprocess.run(["sh","-c","sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/ipy2.sh > ipy2.sh"])

	wired_interface=ask_user_for_interface("\u001b[36mSelect wired interface (#) >> \u001b[0m")
	wireless_interface=ask_user_for_interface("\u001b[36mSelect wireless interface (#) >> \u001b[0m")
	wireless_ipv4_router_addr=input("\u001b[36mgateway ip on wireless network >> \u001b[0m")
	wireless_ipv4_addr=input("\u001b[36mstatic ip on wireless network >> \u001b[0m")
	wireless_ipv4_subnet=input("\u001b[36msubnet mask on wireless network (24 for 255.255.255.0) >> \u001b[0m")
	wired_ipv4_addr=input("\u001b[36mstatic ip on pouter network (eg. 10.0.0.1) >> \u001b[0m")
	wired_ipv4_dhcp_start_addr=input("\u001b[36mdhcp start ip on pouter network (eg. 10.0.0.12) >> \u001b[0m")
	wired_ipv4_dhcp_end_addr=input("\u001b[36mdhcp end ip on pouter network (eg. 10.0.0.169) >> \u001b[0m")

	paa = getpass("\u001b[31mpi-hole web admin password: >> \u001b[0m")

	install_pi_hole(wireless_ipv4_addr, wireless_ipv4_subnet, wired_ipv4_dhcp_start_addr, wired_ipv4_dhcp_end_addr, wired_ipv4_addr, paa, wired_interface, wireless_interface)
	
	base=wired_ipv4_addr.split(".")
	base[-1]="0"
	base=".".join(base)
	runnn_bash(f"sudo iptables -A FORWARD -o {wireless_interface} -i {wired_interface} -s {base}/24 -m conntrack --ctstate NEW -j ACCEPT")
	
	subprocess.run(['sudo',"chmod","+x","ipy2.sh"])
	subprocess.run(['sudo','bash','./ipy2.sh'])

	conf=get_pi_hole_config(wireless_ipv4_addr, wireless_ipv4_subnet, wired_ipv4_dhcp_start_addr, wired_ipv4_dhcp_end_addr, wired_ipv4_addr,"127.0.0.1#5335",wired_interface,wireless_interface)
	
	runnn("sudo rm -rf /etc/pihole/setupVars.conf")
	runnn("mkdir -p /etc/pihole/")
	
	runnn("sudo touch /etc/pihole/setupVars.conf")
	
	with open("/etc/pihole/setupVars.conf","w") as f:
		f.write(conf)
	with open("/etc/systemd/system/pouter.service","w") as f:
		f.write(f"""[Unit]
Description=pouter service
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/ip addr add {wired_ipv4_addr}/24 dev {wired_interface}

[Install]
WantedBy=multi-user.target
""")
	
	runnn("sudo systemctl start pouter.service")
	runnn("sudo systemctl enable pouter.service")
	
	
	args = ["pihole","-a","-p",paa]
	kwargs = dict(stdout=subprocess.PIPE, encoding="ascii")
	cmd = subprocess.run(args)
	with open("/etc/dhcpcd.conf","r") as f:
		l=f.readlines()
		for i,line in enumerate(l):
			if line.startswith("# >>> pouter config >>>"):
				l1=l[:i]
				g=False
				for i2,line2 in enumerate(l1):
					if line2.startswith("# <<< pouter config <<<"):
						l=l1[i2+1:]
						g=True
						break
				if g:
					break
	with open("/etc/dhcpcd.conf","w") as f:
		f.writelines(l)
	with open("/etc/dhcpcd.conf","a") as f:
		f.write(f"""
# >>> pouter config >>>
interface {wireless_interface}
\tstatic ip_address={wireless_ipv4_addr}/{wireless_ipv4_subnet}
\tstatic routers={wireless_ipv4_router_addr}
\tstatic domain_name_servers=
# <<< pouter config <<<
""")
	
	print("Installation successful!")

