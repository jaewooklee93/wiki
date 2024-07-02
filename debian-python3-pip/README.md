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

# .bashrc에서 PATH를 업데이트한다.
$ echo -e '\nexport PATH="$HOME/.venv/bin:$PATH"\n' >> .bashrc

# .bashrc에 잘 반영되었는지 눈으로 확인한다.
$ tail .bashrc
... export PATH="$HOME/.venv/bin:$PATH"

# bash를 새로 열고 잘 되는지 확인한다.
$ bash
$ which python pip
/home/.../.venv/bin/python
/home/.../.venv/bin/pip

# 앞으로 pip을 쓰면 모두 .venv에 깔리지만 내가 신경쓸 것은 없다
pip install streamlit

# 이미 씨스템 파이썬으로 jupyter, streamlit 설치한 경우에도
which jupyter
/home/w/.local/bin/jupyter # 씨스템 파이썬의 잔재
/home/w/.venv/bin/streamlit

# 그냥 새로 깔아서 덮어씌워주면 된다. (PATH 앞쪽에 있어서 우선순위가 우위)
pip install jupyterlab
which jupyter
/home/w/.venv/bin/jupyter
/home/w/.venv/bin/streamlit

``` 