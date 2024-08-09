" 기본 설정
set nocompatible              " Vi 호환 모드 비활성화
set encoding=utf-8            " 파일 인코딩을 UTF-8로 설정

" 탭 및 공백 설정
set tabstop=4                 " 탭을 4칸으로 설정
set shiftwidth=4              " 자동 들여쓰기를 4칸으로 설정
set expandtab                 " 탭 대신 공백 사용

" 줄 번호 표시
set number                    " 줄 번호 표시
" set relativenumber            " 상대 줄 번호 표시

" 검색 설정
set ignorecase                " 대소문자 구분 없이 검색
set smartcase                 " 대문자가 포함되면 대소문자 구분
set incsearch                 " 입력하는 동안 실시간 검색
set hlsearch                  " 검색 결과 하이라이트

" 기타 유용한 설정
" set clipboard=unnamedplus     " 시스템 클립보드 사용
set autoindent                " 자동 들여쓰기
set smartindent               " 스마트 들여쓰기
set wrap                      " 줄 바꿈
" set cursorline                " 현재 줄 강조
set showcmd                   " 명령어 입력 시 상태 표시
set showmatch                 " 괄호 짝 맞추기 강조
set timeoutlen=500            " 키 매핑 대기 시간 설정

" 색상 설정
syntax on                     " 문법 강조 활성화
set background=dark           " 어두운 배경 설정
" colorscheme desert            " 색상 테마 설정 (원하는 테마로 변경 가능)

" 파일 탐색기 설정 (NERDTree 사용 시)
" 플러그인 설치 후 사용
" nmap <C-n> :NERDTreeToggle<CR> " Ctrl+n으로 NERDTree 열기
