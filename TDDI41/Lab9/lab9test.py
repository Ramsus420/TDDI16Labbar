import subprocess

hostname = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True).stdout.strip()


def test_exports():
    result = subprocess.run("cat /etc/exports | grep 10.0.0.0", shell=True, stdout=subprocess.PIPE, text=True)
    assert "rw,sync,no_subtree_check" in result.stdout.strip()

    result = subprocess.run("cat /etc/exports | grep 10.0.0.3", shell=True, stdout=subprocess.PIPE, text=True)
    assert "/home1 10.0.0.3(rw,sync,root_squash,no_subtree_check)" in result.stdout.strip()
    assert "/home2 10.0.0.3(rw,sync,root_squash,no_subtree_check)" in result.stdout.strip()

    result = subprocess.run("cat /etc/exports | grep 10.0.0.4", shell=True, stdout=subprocess.PIPE, text=True)
    assert "/home1 10.0.0.4(rw,sync,root_squash,no_subtree_check)" in result.stdout.strip()
    assert "/home2 10.0.0.4(rw,sync,root_squash,no_subtree_check)" in result.stdout.strip()

    #hittade showmount -e att köra på klienterna men det hänger sig bara.
    #vad är det vi ens ska kolla här?

def server_test_started():
    result = subprocess.run("systemctl status slapd | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()

    result = subprocess.run("systemctl status autofs | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()

    result = subprocess.run("systemctl status nfs-kernel-server | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (exited)" in result.stdout.strip()

def client_test_started():
    result = subprocess.run("systemctl status autofs | grep active", shell=True, stdout=subprocess.PIPE, text=True)
    assert "active (running)" in result.stdout.strip()

def test_firewall():
    result = subprocess.run("cat /etc/nftables.conf | grep tcp", shell=True, stdout=subprocess.PIPE, text=True)
    assert "tcp dport 2049 accept" in result.stdout.strip()
    result = subprocess.run("cat /etc/nftables.conf | grep udp", shell=True, stdout=subprocess.PIPE, text=True)
    assert "udp dport 2049 accept" in result.stdout.strip()



def test_nsswitch():
    result = subprocess.run("cat /etc/nsswitch.conf | grep automount", shell=True, stdout=subprocess.PIPE, text=True)
    assert "ldap" in result.stdout.strip()

def test_mount_local():
    result = subprocess.run("df -h | grep 10.0.0.2:/usr/local", shell=True, stdout=subprocess.PIPE, text=True)
    assert "/mnt/nfs_local" in result.stdout.strip()

def test_ldap_auto():
    result = subprocess.run("automount -m | grep type", shell=True, stdout=subprocess.PIPE, text=True)
    assert "type: ldap" in result.stdout.strip()

if hostname == "server":
    server_test_started()
    test_firewall()
    test_exports()
else:
    test_nsswitch()
    test_mount_local()
    test_ldap_auto()
    client_test_started()