## `app.py`
```python
import json, re, requests

example = '''# LLaMA.cpp HTTP Server

Fast, lightweight, pure C/C++ HTTP server based on [httplib](https://github.com/\
yhirose/cpp-httplib), [nlohmann::json](https://github.com/nlohmann/json) and \
**llama.cpp**.

Set of LLM REST APIs and a simple web front end to interact with llama.cpp.

**Features:**
 * LLM inference of F16 and quantum models on GPU and CPU
 * [OpenAI API](https://github.com/openai/openai-openapi) compatible chat \
completions and embeddings routes
 * Parallel decoding with multi-user support
 * Continuous batching
 * Multimodal (wip)
 * Monitoring endpoints
 * Schema-constrained JSON response format

The project is under active development, and we are [looking for feedback and \
contributors](https://github.com/ggerganov/llama.cpp/issues/4216).'''

prompt = {
    'filename': '/ggerganov/llama.cpp/master/examples/server/README.md',
    'en-US': {'src': example},
    'ko-KR': '%PLACEHOLDER%'
}
prompt = json.dumps(prompt)
prompt = re.sub(' "%PLACEHOLDER%(.*)', '', prompt)
print('\n\tPrompt:\n')
print(prompt)
print('\n---\n')

response = requests.post(
    f'http://localhost:8080/completion',
    stream=True,
    json=dict(
        prompt=prompt,
        stream=True,
        json_schema=dict(
            type='object',
            properties=dict(
                src={'type': 'string'}
            )
        )
    )
)

print('\tResponse:\n')
content = ''
for line in response.iter_lines():
    if line := re.match('data: (.*)', line.decode()):
        line = json.loads(line.group(1))
        print(line['content'], end='', flush=True)
        
        content += line['content']

result = json.loads(content)['src']
print('\n---\n')

print('\tMarkdown:\n')
try:
    # IPython 환경인지 확인
    ipython = get_ipython()
    from IPython.display import Markdown
    display(Markdown(result))
except:
    print(result)
```

## Output
```sh
$ python app.py 

        Prompt:

{"filename": "/ggerganov/llama.cpp/master/examples/server/README.md", "en-US":
{"src": "# LLaMA.cpp HTTP Server  Fast, lightweight, pure C/C++ HTTP server
based on [httplib](https://github.com/yhirose/cpp-httplib),
[nlohmann::json](https://github.com/nlohmann/json) and **llama.cpp**.  Set of
LLM REST APIs and a simple web front end to interact with llama.cpp.
**Features:**  * LLM inference of F16 and quantum models on GPU and CPU  *
[OpenAI API](https://github.com/openai/openai-openapi) compatible chat
completions and embeddings routes  * Parallel decoding with multi-user support
* Continuous batching  * Multimodal (wip)  * Monitoring endpoints  * Schema-
constrained JSON response format  The project is under active development, and
we are [looking for feedback and
contributors](https://github.com/ggerganov/llama.cpp/issues/4216)."}, "ko-KR"

---

        Response:

{"src": "# LLaMA.cpp HTTP 서버
[httplib](https://github.com/yhirose/cpp-httplib),
[nlohmann::json](https://github.com/nlohmann/json) 및 **llama.cpp** 기반의
빠르고 가벼운 순수 C/C++ HTTP 서버입니다. LLM REST API 세트 및 llama.cpp와 상호
작용하기 위한 간단한 웹 프런트 엔드입니다. **특징:** * GPU 및 CPU에서 F16 및
양자 모델의 LLM 유추 * [OpenAI API](https://github.com/openai/openai-openapi)
호환되는 채팅 완성 및 잠재형 엔드포인트 * 다중 사용자 지원을 가진 병렬 디코딩 *
지속적인 배치 처리 * 다중 모달 (준비 중) * 모니터링 엔드포인트 * 스키마 제약
JSON 응답 형식 이 프로젝트는 적극적으로 개발 중이며, [피드백 및 기여자를 찾고
있습니다](https://github.com/ggerganov/llama.cpp/issues/4216)."}

---

        Markdown:
```

## LLaMA.cpp HTTP 서버

[httplib](https://github.com/yhirose/cpp-httplib), [nlohmann::json](https://github.com/nlohmann/json) 및 **llama.cpp** 기반의 빠르고 가벼운 순수 C/C++ HTTP 서버입니다.

LLM REST API 세트 및 llama.cpp와 상호 작용하기 위한 간단한 웹 프런트 엔드입니다.

**특징:**
 * GPU 및 CPU에서 F16 및 양자 모델의 LLM 유추
 * [OpenAI API](https://github.com/openai/openai-openapi) 호환되는 채팅 완성 및 잠재형 엔드포인트
 * 다중 사용자 지원을 가진 병렬 디코딩
 * 지속적인 배치 처리
 * 다중 모달 (준비 중)
 * 모니터링 엔드포인트
 * 스키마 제약 JSON 응답 형식

이 프로젝트는 적극적으로 개발 중이며, [피드백 및 기여자를 찾고 있습니다](https://github.com/ggerganov/llama.cpp/issues/4216).