import random
import subprocess
import sys
import string

generated_usernames = []

def generate_username(name):
    if " " in name:
        splitname = name.split(' ', 2)
        tmpname = splitname[0].lower()[:2] + splitname[1].lower()[:2] + str(random.randint(100, 999))
    else:
        splitname = name
        tmpname = splitname.lower()[:4] + str(random.randint(100, 999))

    for char in tmpname:
        if char not in string.ascii_lowercase + string.digits:
            tmpname = tmpname.replace(char, random.choice(string.ascii_lowercase))

    #om alla användarnamn är upptagna kommer det bli oändlig rekursion
    if tmpname in generated_usernames:
        tmpname = generate_username(name)

    return tmpname


def create_user(username):
    subprocess.run(["ldapadduser", username, "users"])
    #get uid from ldapusern
    uid = subprocess.run(["id", "-u", username], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    #create local user with same uid
    subprocess.run(["useradd", "-u", str(uid), username])


def set_password(username, password):
    #Command to change the ldap user's password
    cmd = ['ldapsetpasswd', username]
    # Running the command and communicating with it
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Sending the password to the command through stdin with pipe
    proc.communicate(input=f'{password}\n{password}\n'.encode('utf-8'))

    #Command to change the local user's password
    cmd = ['passwd', username]
    # Running the command and communicating with it
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Sending the password to the command through stdin with pipe
    proc.communicate(input=f'{password}\n{password}\n'.encode('utf-8'))
    

def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(10))


def main(filename):
    file = open(filename, 'r', encoding='utf-8', errors='ignore')
    names = file.readlines()
    file.close()

    for name in names:
        if name == '\n':
            print("Empty line in file")
            continue
        username = generate_username(name)
        generated_usernames.append(username)
        password = generate_password()
        create_user(username)
        set_password(username, password)
        print(f"User {username} created with password {password}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_accounts.py names.txt")
        sys.exit(1)
    main(sys.argv[1])