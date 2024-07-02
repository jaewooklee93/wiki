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
$ pip install streamlit
```

- 기존 씨스템 파이썬에서 설치한 패키지와 충돌 상황 디버깅
```sh
# 이미 씨스템 파이썬으로 jupyter, streamlit 설치한 경우에도
$ which jupyter
/home/.../.local/bin/jupyter # 씨스템 파이썬의 잔재
/home/.../.venv/bin/streamlit

# 그냥 새로 깔아서 덮어씌워주면 된다. (PATH 앞쪽이라 우선순위 우위)
$ pip install jupyterlab
$ which jupyter
/home/.../.venv/bin/jupyter
/home/.../.venv/bin/streamlit
``` 

- `anaconda`를 사용하던 경우 `.bashrc`에서 >>> 부터 <<< 사이의 내용을 제거해주어야 한다.
- `~/anaconda` 폴더가 있다면 그냥 지워도 된다.
```sh
$ vi ~/.bashrc

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/me/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/me/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/home/me/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/me/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```