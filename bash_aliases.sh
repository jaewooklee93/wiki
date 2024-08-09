export RC="~/.bash_aliases"
alias rc="vi $RC && tail $RC && source $HOME/.${SHELL##*/}rc"

alias l="ls -al --color=auto"
alias ls="ls -al --color=auto"
alias ns="watch -n 0.1 nvidia-smi"
alias log="docker compose logs -f" # compose V2
alias i="sudo apt-get install -y"
alias debian="docker run -it --rm --gpus all python bash"
alias download="huggingface-cli download"
alias journal="sudo journalctl -u"
alias bsah="bash" # common typing error
alias pyhton="python" # common typing error
alias make="make -j"

export GGML_CUDA=1
export LLAMA_CURL=1

export LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/lib:$LD_LIBRARY_PATH"
export PATH="/home/w/.venv/bin:/home/w/hub/llama.cpp:/usr/local/cuda/bin:$PATH"
alias rsync="rsync -avPh"
alias wg="sudo wg"
alias apt="sudo apt-get"
alias dpkg="sudo dpkg"
alias systemctl="sudo systemctl"
alias service="sudo service"

dash() { sudo docker run -it --rm "$1" bash; }
alias nuc="ssh 192.168.12.2"
alias mac="ssh jaewooklee@192.168.12.45"
alias ip="ip -4"
alias ping="ping -c 2"

diff() {
	if [[ $# -eq 0 ]]; then
	      git diff --staged
	else
	      diff -qr "$@"
	fi
}

alias less="less -SEX"

docker() {
	if [[ "$1" == "ps" ]]; then
		command sudo docker ps | less -SEX
	elif [[ "$1" == "rm" ]]; then
		command sudo docker "$@" -f
	else
		command sudo docker "$@"
	fi
}

alias ..="cd .."  # 상위 디렉토리로 이동
alias ...="cd ../.."  # 두 단계 위로 이동
alias ~="cd ~"  # 홈 디렉토리로 이동
alias mkdir="mkdir -p"

alias myip="curl ifconfig.me"  # 내 IP 주소 확인
alias ports="netstat -tuln"  # 열려 있는 포트 확인
alias free="free -h --si"
alias df="df -h"

alias status="git status ."
alias push="git push"
alias pull="git pull"
alias add="git add"

commit() {
	git commit -m "$*"
}

git() {
	if [[ "$1" == "diff" ]]; then
		shift
		command git diff --staged "$@"
	else
		command git "$@"
	fi
}

alias cls="clear"
alias weather="curl ko.wttr.in"
