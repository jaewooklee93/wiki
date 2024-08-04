## `docker-compose.yml`

- host와 격리된 환경에서 `jupyter lab` server가 실행되며, `cuda` 및 `torch`가 미리 설치되어 있음.

- `w`는 본인의 아이디로 변경하여야 함.

- 주피터 내에서 생성한 파일은 `/home/w/dev/sandbox` 폴더에서 확인 가능

- `--IdentityProvider.token=''` 옵션이 있어서 이대로 실행하면 로그인은 없음.

- 그래서 nginx auth 같은 걸로 비밀번호를 한겹 덮어주어야 함

- 이론적으로는 샌드박스만 노출되는거라 그냥 인터넷에 노출시켜도 위험도가 높지는 않으나 혹시 모름.

```yaml
x-defaults: &defaults
  restart: unless-stopped
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]

services:
  jupyter:
    image: quay.io/jupyter/pytorch-notebook
    <<: *defaults
    container_name: jupyter
    volumes:
      - /home/w/dev/sandbox:/home/w
      - /home/w/.jupyter:/home/w/.jupyter
    ports:
      - "8888:8888"
    user: root
    environment:
      - NB_USER=w
      - NB_UID=1000
      - NB_GID=1000
      - CHOWN_HOME=yes
      - GRANT_SUDO=yes
    working_dir: /home/w
    command: start-notebook.py --IdentityProvider.token=''
```
