## Steps
1. elasticsearch server 가동
2. Obsidian Vault를 elasticsearch에 업로드
3. Streamlit app으로 search-as-you-type 구현

## 1. elasticsearch server 가동

### `docker-compose.yml`
```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.14.1
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data

volumes:
  es-data:
```

### PING test

```sh
$ curl http://localhost:9200

{
  "name" : "bb0c7b36b2ec",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "f-t9FuV-T026RGC0nAgQXg",
  "version" : {
    "number" : "8.14.1",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "93a57a1a76f556d8aee6a90d1a95b06187501310",
    "build_date" : "2024-06-10T23:35:17.114581191Z",
    "build_snapshot" : false,
    "lucene_version" : "9.10.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


## 2. Obsidian Vault를 elasticsearch에 업로드

```python
from glob import glob
from elasticsearch import Elasticsearch, helpers
import os

# 자신의 obsidian vault 주소로 변경
md_files = glob('/mnt/c/Users/j/Documents/obsidian-sync/**/*.md', recursive=True) 
md_contents = []
for file_path in md_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        md_contents.append({
            'file_name': os.path.basename(file_path),
            'content': content
        })
md_contents


# Elasticsearch 클라이언트 생성
es = Elasticsearch('http://localhost:9200')

# 인덱스 생성
index_name = 'md_files'
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body={
        'mappings': {
            'properties': {
                'file_name': {'type': 'text'},
                'content': {'type': 'text'}
            }
        }
    })

# 데이터 인덱싱
actions = [
    {
        '_index': index_name,
        '_source': md_content
    }
    for md_content in md_contents
]

helpers.bulk(es, actions)
```

## 3. Streamlit app
```python
# pip install streamlit streamlit-keyup elasticsearch
import streamlit as st
from st_keyup import st_keyup
from elasticsearch import Elasticsearch

st.html("""<style>
    header { visibility: hidden; }
    body { 
        font-family: Pretendard, sans-seif; 
        overflow-x: hidden;
        overflow-y: hidden;
    }
    ::-webkit-scrollbar { display: none; }
    .block-container { padding: 1rem !important; } 
    code {
        white-space: pre-wrap !important;
        font-size: 11px !important;
    }
    * {
      scrollbar-width: none !important; /* Firefox 전용 */
    }
</style>""")

# Elasticsearch 클라이언트 생성
es = Elasticsearch('http://localhost:9200')

# Elasticsearch 클라이언트 설정
index_name = 'md_files'

st.title("🔍 *Jimm* 전용 검색 엔진")


if query := st_keyup("Search-as-you-type", key="0"):
    response = es.search(
        index=index_name,
        body={
            'query': {
                'match': {
                    'content': query
                }
            }
        }
    )

    hits = response['hits']['hits']
    for hit in hits:
        st.write(f"**File Name:** {hit['_source']['file_name']}")
        st.code(f"**Content:** {hit['_source']['content'][:200]}...")  # 첫 200자만 표시
        st.write('---')
```