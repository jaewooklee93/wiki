1. elasticsearch server 가동
2. 

# 1. elasticsearch server 가동

Ref: [Getting started with the Elastic Stack and Docker Compose](https://www.elastic.co/blog/getting-started-with-the-elastic-stack-and-docker-compose)

## 1-1. `docker-compose.yml`
```yaml
version: "3.8"


volumes:
 certs:
   driver: local
 esdata01:
   driver: local
 kibanadata:
   driver: local
 metricbeatdata01:
   driver: local
 filebeatdata01:
   driver: local
 logstashdata01:
   driver: local


networks:
 default:
   name: elastic
   external: false


services:
 setup:
   image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
   volumes:
     - certs:/usr/share/elasticsearch/config/certs
   user: "0"
   command: >
     bash -c '
       if [ x${ELASTIC_PASSWORD} == x ]; then
         echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
         exit 1;
       elif [ x${KIBANA_PASSWORD} == x ]; then
         echo "Set the KIBANA_PASSWORD environment variable in the .env file";
         exit 1;
       fi;
       if [ ! -f config/certs/ca.zip ]; then
         echo "Creating CA";
         bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
         unzip config/certs/ca.zip -d config/certs;
       fi;
       if [ ! -f config/certs/certs.zip ]; then
         echo "Creating certs";
         echo -ne \
         "instances:\n"\
         "  - name: es01\n"\
         "    dns:\n"\
         "      - es01\n"\
         "      - localhost\n"\
         "    ip:\n"\
         "      - 127.0.0.1\n"\
         "  - name: kibana\n"\
         "    dns:\n"\
         "      - kibana\n"\
         "      - localhost\n"\
         "    ip:\n"\
         "      - 127.0.0.1\n"\
         > config/certs/instances.yml;
         bin/elasticsearch-certutil cert --silent --pem -out config/certs/certs.zip --in config/certs/instances.yml --ca-cert config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
         unzip config/certs/certs.zip -d config/certs;
       fi;
       echo "Setting file permissions"
       chown -R root:root config/certs;
       find . -type d -exec chmod 750 \{\} \;;
       find . -type f -exec chmod 640 \{\} \;;
       echo "Waiting for Elasticsearch availability";
       until curl -s --cacert config/certs/ca/ca.crt https://es01:9200 | grep -q "missing authentication credentials"; do sleep 30; done;
       echo "Setting kibana_system password";
       until curl -s -X POST --cacert config/certs/ca/ca.crt -u "elastic:${ELASTIC_PASSWORD}" -H "Content-Type: application/json" https://es01:9200/_security/user/kibana_system/_password -d "{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do sleep 10; done;
       echo "All done!";
     '
   healthcheck:
     test: ["CMD-SHELL", "[ -f config/certs/es01/es01.crt ]"]
     interval: 1s
     timeout: 5s
     retries: 120

 es01:
   depends_on:
     setup:
       condition: service_healthy
   image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
   labels:
     co.elastic.logs/module: elasticsearch
   volumes:
     - certs:/usr/share/elasticsearch/config/certs
     - esdata01:/usr/share/elasticsearch/data
   ports:
     - ${ES_PORT}:9200
   environment:
     - node.name=es01
     - cluster.name=${CLUSTER_NAME}
     - discovery.type=single-node
     - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
     - bootstrap.memory_lock=true
     - xpack.security.enabled=true
     - xpack.security.http.ssl.enabled=true
     - xpack.security.http.ssl.key=certs/es01/es01.key
     - xpack.security.http.ssl.certificate=certs/es01/es01.crt
     - xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
     - xpack.security.transport.ssl.enabled=true
     - xpack.security.transport.ssl.key=certs/es01/es01.key
     - xpack.security.transport.ssl.certificate=certs/es01/es01.crt
     - xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
     - xpack.security.transport.ssl.verification_mode=certificate
     - xpack.license.self_generated.type=${LICENSE}
   mem_limit: ${ES_MEM_LIMIT}
   ulimits:
     memlock:
       soft: -1
       hard: -1
   healthcheck:
     test:
       [
         "CMD-SHELL",
         "curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep -q 'missing authentication credentials'",
       ]
     interval: 10s
     timeout: 10s
     retries: 120
```

## 1-2. `.env`

stack을 생성할때 다음의 .env도 첨부해주어야 한다.

```
# Project namespace (defaults to the current folder name if not set)
#COMPOSE_PROJECT_NAME=myproject


# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=changeme


# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=changeme


# Version of Elastic products
STACK_VERSION=8.7.1


# Set the cluster name
CLUSTER_NAME=docker-cluster


# Set to 'basic' or 'trial' to automatically start the 30-day trial
LICENSE=basic
#LICENSE=trial


# Port to expose Elasticsearch HTTP API to the host
ES_PORT=9200


# Port to expose Kibana to the host
KIBANA_PORT=5601


# Increase or decrease based on the available host memory (in bytes)
ES_MEM_LIMIT=1073741824
KB_MEM_LIMIT=1073741824
LS_MEM_LIMIT=1073741824


# SAMPLE Predefined Key only to be used in POC environments
ENCRYPTION_KEY=c34d38b3a14956121ff2170e5030b471551370178f43e5626eec58b04a30fae2
```

## 1-3. self-signed SSL 인증서 추출
- 첫 실행때 elasticsearch가 SSL 인증서를 생성하는데, 이를 host의 `/tmp/ca.crt` 로 추출한다.
```sh
docker cp elasticstack_docker-es01-1:/usr/share/elasticsearch/config/certs/ca/ca.crt /tmp/.
```
- `elasticstack_docker` 부분은 자신의 stack 이름으로 변경한다.
    - portainer에서는 stack 이름
    - docker compose CLI에서는 docker-compose.yml이 있는 폴더 이름

## 1-4. PING test

```sh
curl -k --cacert /tmp/ca.crt -u elastic:changeme https://localhost:9200
```
![alt text](image4.png)


# 2. Obsidian Vault를 elasticsearch에 업로드

```python
from glob import glob
from elasticsearch import Elasticsearch, ConnectionError, ConnectionTimeout, helpers

# 자신의 obsidian vault 주소로 변경
md_files = glob('/mnt/c/Users/j/Documents/obsidian-sync/**/*.md') 
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
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="/tmp/ca.crt",
    basic_auth=("elastic", "changeme"),
    verify_certs=True
)

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

# 3. Streamlit app
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
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="/tmp/ca.crt",
    basic_auth=("elastic", "changeme"),
    verify_certs=True
)

# Elasticsearch 클라이언트 설정
index_name = 'md_files'

st.title("🔍 *Jimm* 전용 검색 엔진")
query = st_keyup("Search-as-you-type", key="0")

@st.experimental_fragment
def result():
    if query:
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
# with st.container(height=1200):
result()
```