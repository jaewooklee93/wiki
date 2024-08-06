```python
def expose(ngrok_authtoken):
    import subprocess, threading, time
    def bash(script): subprocess.run(script, shell=True)
    def timer(done, s=45):
        for i in range(s+1):
          if done.is_set(): break
          print(f'\rWait for ~ {s} seconds... \x1b[33m{i:>2} s', 
                end='', flush=True)
          time.sleep(1)

    done = threading.Event()
    threading.Thread(target=timer, args=(done,)).start()
    bash('''
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
        	| tee /etc/apt/trusted.gpg.d/ngrok.asc
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
        	| tee /etc/apt/sources.list.d/ngrok.list
        apt-get update && apt-get install -y ngrok 
        pip install jupyterlab pyngrok
    ''')
    from pyngrok import ngrok
    ngrok.set_auth_token(ngrok_authtoken)
    tunnel = ngrok.connect(8888).public_url
    done.set()
    print(f'\r{tunnel}', flush=True)
    try: bash('jupyter lab --IdentityProvider.token=""')
    finally: ngrok.disconnect(tunnel)

expose(ngrok_authtoken='<YOUR_NGROK_AUTHTOKEN>')
# https://dashboard.ngrok.com/get-started/your-authtoken
```