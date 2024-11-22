import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()

#test Är inställd för att göra slagningar mot rätt DNS-server
def test_dns_server_server():
    result = subprocess.run("cat /etc/resolv.conf | grep nameserver", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.2.3")

def test_dns_server_clients():
    result = subprocess.run("cat /etc/resolv.conf | grep nameserver", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.2")




#testa att named/bind9 är rätt konfigurerat
def test_named_bind9_config():
    result = subprocess.run("dig client-1.rasmus.rikard.com | grep ANSWER:", shell=True, stdout=subprocess.PIPE, text=True)
    assert "ANSWER: 1" in result.stdout.strip()
    result = subprocess.run("dig client-1.rasmus.rikard.com | grep SERVER:", shell=True, stdout=subprocess.PIPE, text=True)
    assert "SERVER: 10.0.0.2" in result.stdout.strip()
    result = subprocess.run("cat /etc/bind/named.conf.options | grep query", shell=True, stdout=subprocess.PIPE, text=True)
    assert "allow-query" in result.stdout.strip()
    result = subprocess.run("cat /etc/bind/named.conf.options | grep recursion", shell=True, stdout=subprocess.PIPE, text=True)
    assert "allow-recursion" in result.stdout.strip()


#testa brandvägg med grep
def test_firewall():
    result = subprocess.run("cat /etc/nftables.conf | grep tcp", shell=True, stdout=subprocess.PIPE, text=True)
    assert "tcp dport 53 accept" in result.stdout.strip()
    result = subprocess.run("cat /etc/nftables.conf | grep udp", shell=True, stdout=subprocess.PIPE, text=True)
    assert "udp dport 53 accept" in result.stdout.strip()


#testa att servern har korrekta och hela zonfiler
def test_zone_files():
    result = subprocess.run("named-checkconf /etc/bind/named.conf.local", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0
    result = subprocess.run("named-checkconf /etc/bind/named.conf.options", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0
    result = subprocess.run("named-checkzone rasmus.rikard.com /etc/bind/zones/rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0
    result = subprocess.run("named-checkzone rev.0.0.10 /etc/bind/zones/reverse/rev.0.0.10", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0

#test har named körandes utan problem
def test_named_running():
    result = subprocess.run("systemctl status bind9 | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()


#testa att alla svarar korrekt på dns-frågor forward och backwards
def test_dns_forward():
    result = subprocess.run("host rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.2")
    result = subprocess.run("host server.rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.2")
    result = subprocess.run("host client-1.rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.3")
    result = subprocess.run("host client-2.rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.4")
    result = subprocess.run("host gw.rasmus.rikard.com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("10.0.0.1")

def test_dns_reverse():
    result = subprocess.run("host 10.0.0.1", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("gw.rasmus.rikard.com.")
    result = subprocess.run("host 10.0.0.2", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("rasmus.rikard.com.")
    result = subprocess.run("host 10.0.0.3", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("client-1.rasmus.rikard.com.")
    result = subprocess.run("host 10.0.0.4", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("client-2.rasmus.rikard.com.")


if hostname == "server":
    test_dns_server_server()

    test_named_bind9_config()
    test_firewall()
    test_zone_files()
    test_named_running()

    test_dns_forward()
    test_dns_reverse()
else:
    test_dns_server_clients()

    test_dns_forward()
    test_dns_reverse()