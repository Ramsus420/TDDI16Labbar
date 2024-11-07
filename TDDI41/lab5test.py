import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()

def test_check_netmask():
    result = subprocess.run("cat /etc/network/interfaces | grep netmask", shell=True, stdout=subprocess.PIPE, text=True)
    
    assert result.stdout.strip().endswith("255.255.255.0")

def test_check_gateway():
        
    if hostname == "gw":
        result = subprocess.run("ip route show | grep default", shell=True, stdout=subprocess.PIPE, text=True)
        assert "10.0.2.2" in result.stdout.strip()
    else:
        result = subprocess.run("cat /etc/network/interfaces | grep gateway", shell=True, stdout=subprocess.PIPE, text=True)
        assert result.stdout.strip().endswith("10.0.0.1")

def test_check_ip():
    result = subprocess.run("cat /etc/network/interfaces | grep address", shell=True, stdout=subprocess.PIPE, text=True)
    if hostname == "gw":
        assert result.stdout.strip().endswith("10.0.0.1")
    elif hostname == "client-1":
        assert result.stdout.strip().endswith("10.0.0.3")
    elif hostname == "client-2":
        assert result.stdout.strip().endswith("10.0.0.4")
    elif hostname == "server":
        assert result.stdout.strip().endswith("10.0.0.2")
    else:
        print("Unknown hostname")
        assert False

def test_connectivity():
    if hostname == "gw":
        result = subprocess.run("ping -c 1 -w 1 10.0.2.2", shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0
    else:
        result = subprocess.run("ping -c 1 -w 1 10.0.0.1", shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0

def test_ip_forward_enable():
    result = subprocess.run("sysctl net.ipv4.ip_forward", shell=True, stdout=subprocess.PIPE, text=True)
    assert "net.ipv4.ip_forward = 1" in result.stdout.strip()

def test_ip_masquerading():
    #kanske funkar??
    result = subprocess.run("iptables -t nat -L POSTROUTING -n", shell=True, stdout=subprocess.PIPE, text=True)
    assert "MASQUERADE" in result.stdout.strip()

def test_firewall_rules():
    #testa ping till alla andra maskiner
    #testa ssh trafik till alla andra maskiner på normala ssh porten
    #testa att inte http trafik funkar till alla andra maskiner

if hostname != "gw" and hostname != "client-1" and hostname != "client-2" and hostname != "server":
    print("Unknown hostname")
    assert False
else:
    print("Running tests for " + hostname)
    test_check_netmask()
    print("Test check netmask passed")
    test_check_gateway()
    print("Test check gateway passed")
    test_check_ip()
    print("Test check ip passed")
    test_connectivity()
    print("Test connectivity passed")
    if hostname == "gw":
        test_ip_forward_enable()
        print("Test ip forward enable passed")
        test_ip_masquerading()
        print("Test ip masquerading passed")
        test_firewall_rules()
        print("Test firewall rules passed")
    print("All tests passed")