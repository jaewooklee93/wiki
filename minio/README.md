## Windows 환경에서 MinIO 서버 설치하기
- Reference: [minio/minio-service](https://github.com/minio/minio-service/blob/master/windows/README.md)

1. `minio.exe`를 다운로드 받는다. 파일 1개에 다 들어 있어 편리하다.
    https://dl.min.io/server/minio/release/windows-amd64/minio.exe

2. Windows cmd에서는 다음과 같이 실행할 수 있다.

    ```cmd
    .\minio.exe server C:\minio --console-address :9001
    ```
    - API: `:9000` (default)
    - WebUI: `:9001`
    - RootUser: `minioadmin` (default)
    - RootPass: `minioadmin` (default)
    - `C:\minio`에 실제 데이터가 저장된다.

3. http://localhost:9001 admin 페이지에 접속하여 bucket, client 생성을 할 수 있다. 

4. http://localhost:9000 으로 API 요청을 할 수 있다.

## autostart on reboot 세팅

1. `minio.exe`를 윈도우 서비스로 등록하기 위해 `WinSW-x64.exe`를 다운 받는다. 역시 파일 1개에 다 들어있다.
    https://github.com/winsw/winsw/releases

2. `MinIO` 폴더를 만들고, `minio.exe` 파일을 복사하고, `WinSW-x64.exe`를 `minio-service.exe`로 rename 하고, 새로 `minio-service.xml` 파일을 만든다. 폴더 트리는 아래와 같이 된다.

    ```
    MinIO
    ├── minio.exe
    ├── minio-service.exe
    └── minio-service.xml
    ```

3. minio-service.xml 파일의 내용을 작성한다.

    ```xml
    <service>
    <id>MinIO</id>
    <name>MinIO</name>
    <description>MinIO is a high performance object storage server</description>
    <executable>minio.exe</executable>
    <env name="MINIO_ROOT_USER" value="minio"/>
    <env name="MINIO_ROOT_PASSWORD" value="minio123"/>
    <arguments>server C:\minio</arguments>
    <logmode>rotate</logmode>
    </service>
    ```
    - API: `:9000` (default)
    - WebUI: `:40154` (자동 생성됨)
    - RootUser: `minio`
    - RootPass: `minio123`
    - `C:\minio`에 실제 데이터가 저장된다.

    여기에서는 <arguments>로 `--console-address :9001`를 명시하지 않았으나 브라우저에서 `http://localhost:9000` 접속하면 자동생성된 port (ex. `http://localhost:40154`)로 redirect되어 간편하다.

4. 폴더를 C:\Program Files\MinIO로 복사하고 관리자 CMD에서 아래와 같이 MinIO 서비스를 설치, 시작, 중단, 재시작, 삭제 할수 있다.
    ```cmd
    cd C:\Program Files\MinIO

    minio-service.exe install
    minio-service.exe start

    minio-service.exe stop
    minio-service.exe restart
    minio-service.exe uninstall
    ```
    이제 MinIO 서버가 Windows 로그인시 자동으로 시작된다.