import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()


def test_firewall():
    result = subprocess.run("cat /etc/nftables.conf | grep 123", shell=True, stdout=subprocess.PIPE, text=True)
    assert "udp dport 123 accept" in result.stdout.strip()

def test_status_running():
    result = subprocess.run("systemctl status ntp | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()


def test_gw_config():
    result = subprocess.run("cat /etc/ntp.conf | grep se.pool", shell=True, stdout=subprocess.PIPE, text=True)
    assert "server se.pool.ntp.org iburst prefer" in result.stdout.strip()

def test_client_config():
    result = subprocess.run("cat /etc/ntp.conf | grep 10.0.0.1", shell=True, stdout=subprocess.PIPE, text=True)
    assert "server 10.0.0.1 iburst prefer" in result.stdout.strip()

def test_query():
    result = subprocess.run("ntpq -p | grep gw", shell=True, stdout=subprocess.PIPE, text=True)
    assert "*gw.rasmus" in result.stdout.strip()

def test_offset():
    result = subprocess.run("ntpq -p | grep gw", shell=True, stdout=subprocess.PIPE, text=True)
    offset = result.stdout.strip().split()[9]
    assert float(offset) < 8.0


if hostname == "gw":
    test_status_running()
    test_gw_config()
    test_firewall()

else:
    test_status_running()
    test_client_config()
    test_query()
    test_offset()
    test_firewall()