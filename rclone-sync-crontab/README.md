## Linux에서 `rclone sync` 주기적으로 자동 실행하기
이 문서는 `rclone`을 사용하여 매일 특정 시간에 자동으로 파일을 동기화하는 방법을 설명합니다.
1. 먼저 `rclone`의 경로를 확인합니다. 터미널에서 다음 명령어를 실행하세요:
    ```sh
    $ which rclone
    /usr/bin/rclone
    ```

2. 터미널을 열고 명령어를 입력하여 crontab 파일을 엽니다:
    ```sh
    crontab -e
    ```

3. 새 cron 작업 추가:
    ```sh
    0 2 * * * /usr/bin/rclone sync /home/w/dev minio:dev
    ```
    - `0 2 * * *`: 매일 오전 2시에 실행
    - `rclone`을 사용하여 `/home/w/dev` 디렉토리를 `minio:dev`로 동기화

4. 편집한 파일의 Syntax 확인
    ```sh
    crontab -l | crontab -n -
    ```