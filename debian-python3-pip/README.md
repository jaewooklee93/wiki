- Debian 계열 distro는 공히 모두 해당된다.
    - Ubuntu
    - Linux Mint
    - Kali Linux

```sh
$ sudo apt update && sudo apt install -y python3-dev python3-venv

# 현 상태 점검
$ which python pip python3 pip3
/usr/bin/python3 # 씨스템 파이썬

# 홈폴더로 간다
$ cd

# venv이름 앞에 .을 붙여야 리눅스 숨김폴더라 눈에 안거슬림
$ python3 -m venv .venv

$ echo -e '\nexport PATH="$HOME/.venv/bin:$PATH"\n' >> .bashrc

# 눈으로 확인
$ tail .bashrc
...
export PATH="$HOME/.venv/bin:$PATH"

# .bashrc 반영후 잘 됐는지 확인
$ bash
$ which python pip
/home/.../.venv/bin/python
/home/.../.venv/bin/pip

# 앞으로 pip을 쓰면 모두 .venv에 깔리지만 내가 신경쓸 것은 없다
pip install streamlit
``` 