import random
import subprocess
import sys
import string


def generate_username(name):
    if " " in name:
        splitname = name.split(' ', 2)
        tmpname = splitname[0].lower()[:2] + splitname[1].lower()[:2] + str(random.randint(100, 999))
    else:
        splitname = name
        tmpname = splitname.lower()[:4] + str(random.randint(100, 999))
    return tmpname


def create_user(username):
    subprocess.run(["useradd", "-m", username])


def set_password(username, password):
    subprocess.run()
    

def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(10))


def main(filename):
    file = open(filename, 'r', encoding='utf-8', errors='ignore')
    names = file.readlines()
    file.close()

    for name in names:
        username = generate_username(name)
        password = generate_password()
        create_user(username)
        set_password(username, password)
        print(f"User {username} created with password {password}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_accounts.py ")
        sys.exit(1)
    main(sys.argv[1])