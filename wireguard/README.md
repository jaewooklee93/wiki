## Wireguard auto-config script

- Client는 Server를 볼 수 있지만, Server는 Client를 볼 수 없는 경우,
VPN 연결을 생성하면 Server도 Client를 볼 수 있게 됩니다.

- 아래의 명령어로 wireguard.py를 다운로드 받습니다.
```sh
wget -q -O wireguard.py \
https://raw.githubusercontent.com/jaewooklee93/wiki/master/wireguard/wireguard.py
chmod +x wireguard.py

```

- 아래의 코드에서 IP를 자신의 server의 IP로 변경하여 실행합니다.
```sh
./wireguard.py 192.168.12.2 # CHANGE
```
- 현재 폴더에 `./server`, `./client` 파일이 생성됩니다. 각각을 server와 client의 컴퓨터에 복사하여 실행합니다.


### Client (`<Unknown>` -> `10.0.0.2`)

```sh
# server측 51820/udp 포트 접근가능여부 확인
sudo nmap 192.168.12.2 -p 51820 -sU

chmod +x client
./client # 연결 개시

# 18000번 포트로 HTTP 서버 시작
python -m http.server 18000

./client down # 연결 해제
```

### Server (`192.168.12.2` -> `10.0.0.1`)

```sh
chmod +x server
./server # 연결 개시

curl 10.0.0.2:18000 
# 반대로 client 측에서 10.0.0.1로 server에 접속하는 것도 가능

./server down # 연결 해제
```
