## `docker-compose.yml`: llama.cpp CUDA server
```yml
services:
  gemma:
    image: ghcr.io/ggerganov/llama.cpp:server-cuda
    ports:
      - "8080:8080"
    volumes:
      - llama-cache:/root/.cache/llama.cpp
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    command: >
      --host 0.0.0.0
      --hf-repo bartowski/gemma-2-9b-it-GGUF
      --hf-file gemma-2-9b-it-IQ4_XS.gguf
      --gpu-layers 99
      --main-gpu 0
volumes:
  llama-cache:
```

## cURL test

```bash
$ curl --request POST \
    --url http://localhost:8080/completion \
    --header "Content-Type: application/json" \
    --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'
```

```javascript
{"content":"\n\n**1. Define Your Purpose:**\n\n* What do you want to achieve with your website?", ... }
```

## Python Client

```python
import requests
response = requests.post(
    'http://localhost:8080/completion',
    json={"prompt": "Building a website can be done in 10 simple steps:",
          "n_predict": 128}
).json()

print(response['content'])
````

```
**1. Define Your Purpose:**

* What do you want to achieve with your website? (e.g., sell products, share information, build a community)
* Who is your target audience?

**2. Choose a Domain Name:**

...
```

## Single token prediction with probs

```sh
pip install requests polars
```

```python
import requests
import polars as pl
pl.Config.set_tbl_rows(40)
response = requests.post(
    'http://localhost:8080/completion',
    json={"prompt": prompt,
          "temperature": -1,
          "n_predict": 1,
          "n_probs":40
         }
).json()

df = pl.DataFrame(response['completion_probabilities'][0]['probs'])
print(df)
```

```
shape: (40, 2)
┌─────────┬──────────┐
│ tok_str ┆ prob     │
│ ---     ┆ ---      │
│ str     ┆ f64      │
╞═════════╪══════════╡
│ D       ┆ 0.996538 │
│ **      ┆ 0.002495 │
│  **     ┆ 0.000539 │
│ C       ┆ 0.000053 │
│ B       ┆ 0.000047 │
│ A       ┆ 0.000032 │
│  D      ┆ 0.000029 │
│ **(     ┆ 0.000024 │
│ d       ┆ 0.000024 │
│ **)     ┆ 0.00002  │
│ E       ┆ 0.000017 │
│ Seoul   ┆ 0.000015 │
│ ㄷ      ┆ 0.000008 │
│ ㄹ      ┆ 0.000007 │
│ 주      ┆ 0.000006 │
│ Д       ┆ 0.000004 │
│ **,     ┆ 0.000004 │
│ 답      ┆ 0.000004 │
│ 디      ┆ 0.000004 │
│ 도      ┆ 0.000004 │
│ ㅁ      ┆ 0.000003 │
│ Ｄ      ┆ 0.000003 │
│ Answer  ┆ 0.000003 │
│ 가      ┆ 0.000003 │
│  )      ┆ 0.000003 │
│ ④       ┆ 0.000003 │
│ )**     ┆ 0.000003 │
│ ד       ┆ 0.000003 │
│ ****    ┆ 0.000003 │
│ ㄱ      ┆ 0.000002 │
│ 다      ┆ 0.000002 │
│ 을      ┆ 0.000002 │
│ ㅇ      ┆ 0.000002 │
│ 유      ┆ 0.000002 │
│ Korean  ┆ 0.000002 │
│ 4       ┆ 0.000002 │
│ G       ┆ 0.000002 │
│ 이      ┆ 0.000001 │
│ ***     ┆ 0.000001 │
│ 하      ┆ 0.000001 │
└─────────┴──────────┘
```