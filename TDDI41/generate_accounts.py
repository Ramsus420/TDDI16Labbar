import random

file = open('/courses/TDDI41/names-tricky', 'r', encoding='utf-8', errors='ignore')

names = file.readlines()

file.close()

accountnames = []


for name in names:
    if " " in name:
        splitname = name.split(' ', 2)
        tmpname = splitname[0].lower()[:2] + splitname[1].lower()[:2] + str(random.randint(100, 999))
    else:
        splitname = name
        tmpname = splitname.lower()[:4] + str(random.randint(100, 999))
    
    ##här skulle vi kunna kontrollera för dubletter
    #om dublett ta bort sista siffror och lägg till nytt random nummer
    accountnames.append(tmpname)


print("hello world")

print(names)

print(accountnames)


