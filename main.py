#!/usr/bin/env python3
import os, subprocess
from getpass import getpass

def is_root():
    return os.geteuid() == 0

def test_sudo(pwd=""):
    args = "sudo -S echo OK".split()
    kwargs = dict(stdout=subprocess.PIPE,
                  encoding="ascii")
    if pwd:
        kwargs.update(input=pwd)
    cmd = subprocess.run(args, **kwargs)
    return ("OK" in cmd.stdout)

def prompt_sudo():
    ok = is_root() or test_sudo()
    return ok
def get_pi_hole_config(wlan0_ipv4_addr,wlan0_ipv4_subnet,eth0_ipv4_dhcp_start_addr,eth0_ipv4_dhcp_end_addr,eth0_ipv4_addr,dns):
    return f"""QUERY_LOGGING=true
PIHOLE_INTERFACE=wlan0
IPV4_ADDRESS={wlan0_ipv4_addr}/{wlan0_ipv4_subnet}
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
DHCP_START={eth0_ipv4_dhcp_start_addr}
DHCP_END={eth0_ipv4_dhcp_end_addr}
DHCP_ROUTER={eth0_ipv4_addr}
DHCP_LEASETIME=0
PIHOLE_DOMAIN=lan
DHCP_IPv6=false
DHCP_rapid_commit=false
API_EXCLUDE_DOMAINS=
API_EXCLUDE_CLIENTS=
API_QUERY_LOG_SHOW=all
"""

unbound_conf="""server:
    # If no logfile is specified, syslog is used
    # logfile: "/var/log/unbound/unbound.log"
    verbosity: 0

    interface: 127.0.0.1
    port: 5335
    do-ip4: yes
    do-udp: yes
    do-tcp: yes

    # May be set to yes if you have IPv6 connectivity
    do-ip6: no

    # You want to leave this to no unless you have *native* IPv6. With 6to4 and
    # Terredo tunnels your web browser should favor IPv4 for the same reasons
    prefer-ip6: no

    # Use this only when you downloaded the list of primary root servers!
    # If you use the default dns-root-data package, unbound will find it automatically
    #root-hints: "/var/lib/unbound/root.hints"

    # Trust glue only if it is within the server's authority
    harden-glue: yes

    # Require DNSSEC data for trust-anchored zones, if such data is absent, the zone becomes BOGUS
    harden-dnssec-stripped: yes

    # Don't use Capitalization randomization as it known to cause DNSSEC issues sometimes
    # see https://discourse.pi-hole.net/t/unbound-stubby-or-dnscrypt-proxy/9378 for further details
    use-caps-for-id: no

    #just don't touch
    edns-buffer-size: 1232

    # Perform prefetching of close to expired message cache entries
    # This only applies to domains that have been frequently queried
    prefetch: yes

    # One thread should be sufficient, can be increased on beefy machines. In reality for most users running on small networks or on a single machine, it should be unnecessary to seek performance enhancement by increasing num-threads above 1.
    num-threads: 1

    # Ensure kernel buffer is large enough to not lose messages in traffic spikes
    so-rcvbuf: 1m

    # Ensure privacy of local IP ranges
    private-address: 192.168.0.0/16
    private-address: 169.254.0.0/16
    private-address: 172.16.0.0/12
    private-address: 10.0.0.0/8
    private-address: fd00::/8
    private-address: fe80::/10
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


def install_pi_hole(wlan0_ipv4_addr, wlan0_ipv4_subnet, eth0_ipv4_dhcp_start_addr, eth0_ipv4_dhcp_end_addr, eth0_ipv4_addr,password):
    conf=get_pi_hole_config(wlan0_ipv4_addr, wlan0_ipv4_subnet, eth0_ipv4_dhcp_start_addr, eth0_ipv4_dhcp_end_addr, eth0_ipv4_addr,"1.1.1.1")
    runnn("rm -rf /etc/pihole/setupVars.conf")
    runnn("mkdir -p /etc/pihole/")
    with open("/etc/pihole/setupVars.conf","w") as f:
        f.write(conf)
    subprocess.run(['sudo',"chmod","+x","ipy.sh"])
    subprocess.run(['sudo','bash','./ipy.sh'])

    args = ["pihole","-a","-p",password]
    kwargs = dict(stdout=subprocess.PIPE,
                encoding="ascii")
    cmd = subprocess.run(args)

    runnn("rm -rf /etc/unbound/unbound.conf.d/pi-hole.conf")
    runnn("mkdir -p /etc/unbound/unbound.conf.d/")
    with open("/etc/unbound/unbound.conf.d/pi-hole.conf","w") as f:
        f.write(unbound_conf)
    runnn(f"sudo ip addr add {eth0_ipv4_addr}/24 dev eth0")
    
    
if __name__ == '__main__':
    print("Welcome to pouter setup")
    if prompt_sudo():
        print("sudo privileges to setup have been given")
            
        subprocess.run(["sh","-c","sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/ipy.sh > ipy.sh"])
        subprocess.run(["sh","-c","sudo curl -sSL https://raw.githubusercontent.com/silverace71/pouter/main/ipy2.sh > ipy2.sh"])
        runnn("sudo apt install -y iptables")
        
        wlan0_ipv4_router_addr=input("\u001b[36mgateway ip on parent network >> \u001b[0m")
        wlan0_ipv4_addr=input("\u001b[36mstatic ip on parent network >> \u001b[0m")
        wlan0_ipv4_subnet=input("\u001b[36msubnet mask on parent network (24 for 255.255.255.0) >> \u001b[0m")
        eth0_ipv4_addr=input("\u001b[36mstatic ip on pouter network (eg. 10.0.0.1) >> \u001b[0m")
        eth0_ipv4_dhcp_start_addr=input("\u001b[36mdhcp start ip on pouter network (eg. 10.0.0.12) >> \u001b[0m")
        eth0_ipv4_dhcp_end_addr=input("\u001b[36mdhcp end ip on pouter network (eg. 10.0.0.169) >> \u001b[0m")
        paa = getpass("\u001b[31mpi-hole web admin password: >> \u001b[0m")
        install_pi_hole(wlan0_ipv4_addr, wlan0_ipv4_subnet, eth0_ipv4_dhcp_start_addr, eth0_ipv4_dhcp_end_addr, eth0_ipv4_addr, paa)
        runnn("sudo apt install -y unbound")
        base=eth0_ipv4_addr.split(".")
        base[-1]="0"
        base=".".join(base)
        runnn_bash(f"sudo iptables -A FORWARD -o wlan0 -i eth0 -s {base}/24 -m conntrack --ctstate NEW -j ACCEPT")
        
        subprocess.run(['sudo',"chmod","+x","ipy2.sh"])
        subprocess.run(['sudo','bash','./ipy2.sh'])

        conf=get_pi_hole_config(wlan0_ipv4_addr, wlan0_ipv4_subnet, eth0_ipv4_dhcp_start_addr, eth0_ipv4_dhcp_end_addr, eth0_ipv4_addr,"127.0.0.1#5335")
        runnn("rm -rf /etc/pihole/setupVars.conf")
        runnn("mkdir -p /etc/pihole/")
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
ExecStart=/usr/bin/ip addr add {eth0_ipv4_addr}/24 dev eth0

[Install]
WantedBy=multi-user.target
""")
        runnn("sudo systemctl start pouter.service")
        runnn("sudo systemctl enable pouter.service")
        args = ["pihole","-a","-p",paa]
        kwargs = dict(stdout=subprocess.PIPE,
                    encoding="ascii")
        cmd = subprocess.run(args)
        with open("/etc/dhcpcd.conf","a") as f:
            f.write(f"""
interface wlan0
\tstatic ip_address={wlan0_ipv4_addr}/{wlan0_ipv4_subnet}
\tstatic routers={wlan0_ipv4_router_addr}
\tstatic domain_name_servers=
""")
        
        for i in range(10):
            print("SUCSSES",end=" ")

    else:
        print("pouter needs sudo privileges to setup")