import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()




def test_started    ():
    result = subprocess.run("systemctl status slapd | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()




if hostname == "server":
    test_started()
else:
    