import pytest
import subprocess

def test_root_entry_in_passwd():
    result = subprocess.run("cat /etc/passwd | grep root", shell=True, stdout=subprocess.PIPE, text=True)
    
    assert result.returncode == 0

def test_games_has_no_shell():

    result = subprocess.run("cat /etc/passwd | grep games", shell=True, stdout=subprocess.PIPE, text=True)
    
    assert result.stdout.strip().endswith("/usr/sbin/nologin")