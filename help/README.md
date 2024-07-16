## `help.py`
```python
#!/usr/bin/python3

import sys, requests, textwrap, json, rich, os, getpass, socket, os
from rich import print

if __name__ == "__main__":
    prompt = ' '.join(sys.argv[1:])
    if prompt.strip():
        response = requests.post(
            f'http://localhost:8080/completion',
            json={
                'prompt': textwrap.dedent(f"""{{'user_request': {prompt}}}
                Provide a bash script (simple, mostly one-liner)
                {{'analyzed_user_intent': '...(in English)', 'bash_program': '[^\s]+(without argument)' 'script': '...(will be executed as-is, without modification)', 'description': '... (in Korean)' }}
                format의 JSON으로 응답하시오."""),
                'json_schema': {}
            }
        ).json()
        response = json.loads(response['content'])
        print()
        print(f"\t[yellow1]({response['analyzed_user_intent']})")
        print()
        print(f"\t[spring_green1]$ {response['script']}")
        print()
        print(f"\t[sky_blue1]- {response['description']}")
        print()
        print('\t[sky_blue1]실행하시겠습니까? (y/N)', end='')
        user = input('')
        script = response['script']
        
        if len(user) and user[0] == 'y':
            user = getpass.getuser()
            hostname = socket.gethostname()
            pwd = os.getcwd().replace(f'/home/{user}', '~')
            head = f'[bright_green]{user}@{hostname}[white]:[bright_blue]{pwd}[spring_green1]$ '
            
            print(f'\n{head}{script}')
            print()
            os.system(script)
```

```sh
$ alias help='python3 ./help.py'
$ help 이 폴더 안에 있는 .md 파일 다 찾기

        (The user wants to find all .md files in the current directory.)

        $ find . -name '*.md'

        - 현재 디렉토리에 있는 모든 .md 파일을 찾습니다.

        실행하시겠습니까? (y/N)y

w@j:~/hub/book$ find . -name '*.md'

./style-guide.md
./CONTRIBUTING.md
./README.md
./.github/ISSUE_TEMPLATE/bug_report.md
./.github/ISSUE_TEMPLATE/new_translation.md
./TODO.md
./first-edition/src/functions.md
./first-edition/src/documentation.md
./first-edition/src/guessing-game.md
./first-edition/src/primitive-types.md
./first-edition/src/conditional-compilation.md
./first-edition/src/the-stack-and-the-heap.md
./first-edition/src/choosing-your-guarantees.md
./first-edition/src/if-let.md
./first-edition/src/concurrency.md
./first-edition/src/match.md
./first-edition/src/method-syntax.md
./first-edition/src/getting-started.md

...
```