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
    result = subprocess.run("cat /etc/bind/named.conf.options | grep forwarde", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("")


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
    result = subprocess.run("systemctl status bind9 | grep Active", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip().endswith("active (running)")


#testa att alla svarar korrekt på dns-frågor forward och backwards
def test_dns_forward():
    result = subprocess.run("", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0

def test_dns_reverse():
    result = subprocess.run("", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0


if hostname == "server":
    test_dns_server_server()
    test_named_bind9_config()
    test_zone_files()
    test_named_running()
    test_dns_forward()
    test_dns_reverse()
else:
    test_dns_server_clients()
    test_dns_forward()
    test_dns_reverse()