import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()




def test_started():
    result = subprocess.run("systemctl status slapd | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()

def test_nsswitch():
    result = subprocess.run("cat /etc/nsswitch.conf | grep passwd", shell=True, stdout=subprocess.PIPE, text=True)
    assert "ldap" in result.stdout.strip()

def test_ldapsearch():
    result = subprocess.run("ldapsearch -x -LLL -H ldap://10.0.0.2 -b dc=rasmus,dc=rikard,dc=com", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.returncode == 0

if hostname == "server":
    test_started()
else:
    test_nsswitch()
    test_ldapsearch()
    