## Wireguard auto-config script

- Client는 Server를 볼 수 있지만, Server는 Client를 볼 수 없는 경우에 사용 가능합니다.

```sh
wget https://raw.githubusercontent.com/jaewooklee93/wiki/master/wireguard/wireguard.py
chmod +x wireguard.py
./wireguard.py 192.168.12.2 # server의 IP 또는 도메인 주소로 번경
```
현재 폴더에 `./server`, `./client` 파일이 생성됩니다. 각각을 server와 client의 컴퓨터에 복사하여 실행합니다.

### Server (`192.168.12.2`:`10.0.0.1`)
```sh
chmod +x server
./server # 연결 개시
./server # 연결 상태 확인

python -m http.server # 8000번 포트로 HTTP 서버 시작

./server down # 연결 해제
```

### Client (`<Unknown>`:`10.0.0.2`)
```sh
nmap 192.168.12.2 -p 51820 -sU # 51820/udp 포트의 접근가능 여부 확인

chmod +x client
./client # 연결 개시
./client # 연결 상태 확인

curl 10.0.0.1:8000 # 반대로 server 측에서 10.0.0.2:8000도 가능

./client down # 연결 해제
```