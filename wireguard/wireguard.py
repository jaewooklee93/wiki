#!/usr/bin/env python

import sys, os

CYAN, YELLOW, WHITE = '\x1b[36m', '\x1b[33m', '\x1b[0m'

def dedent(text):
    return '\n'.join(
        line.lstrip() for line in text.splitlines()
    )

def keygen():
    if os.system('wg --version >/dev/null'):
        print(dedent(f'''\n
        🚨  Ensure that WireGuard is installed on your system.
        
        {YELLOW}sudo apt update && sudo apt install -y wireguard\n
        '''))
        exit(-1)
        
    private = os.popen('wg genkey').read().strip()
    
    return dict(
        private=private,
        public=os.popen(f'echo {private} | wg pubkey').read().strip()
    )
    
def generate_config(server_ip, server_port=51820):
    server_key, client_key = keygen(), keygen()

    with open('server', 'w') as f:
        f.write(dedent(f'''\
            #!/bin/sh

            wg --version >/dev/null
            if [ $? -ne 0 ]; then
                sudo apt update && sudo apt install -y wireguard
            fi
            
            mkdir -p ~/.wg
            
            cat > ~/.wg/server.conf <<EOF
            [Interface]
            PrivateKey = {server_key['private']}
            Address = 10.0.0.1/24
            ListenPort = {server_port}
            
            [Peer]
            PublicKey = {client_key['public']}
            AllowedIPs = 10.0.0.0/24
            EOF

            chmod 600 ~/.wg/server.conf
        
            sudo wg showconf server >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                if [ "$1" = "down" ]; then
                    sudo wg-quick down ~/.wg/server.conf >/dev/null 2>&1
                    echo "interface: server deleted"
                else
                    echo
                    sudo wg
                    echo
                fi
            else
                if [ "$1" = "down" ]; then
                    echo "no interface: server"
                else
                    sudo wg-quick up ~/.wg/server.conf >/dev/null 2>&1
                    echo
                    echo "interface: server created"
                    echo
                    sudo wg
                    echo
                fi
            fi
        '''))
        
    with open('client', 'w') as f:
        f.write(dedent(f'''\
            #!/bin/sh
            
            wg --version >/dev/null
            if [ $? -ne 0 ]; then
                sudo apt update && sudo apt install -y wireguard
            fi
            
            mkdir -p ~/.wg
            
            cat > ~/.wg/client.conf <<EOF
            [Interface]
            PrivateKey = {client_key['private']}
            Address = 10.0.0.2/24
            
            [Peer]
            PublicKey = {server_key['public']}
            Endpoint = {server_ip}:{server_port}
            AllowedIPs = 10.0.0.1/32
            PersistentKeepalive = 25
            EOF
            
            chmod 600 ~/.wg/client.conf
            
            sudo wg showconf client >/dev/null >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                if [ "$1" = "down" ]; then
                    sudo wg-quick down ~/.wg/client.conf >/dev/null 2>&1
                    echo "interface: client deleted"
                else
                    echo
                    sudo wg
                    echo
                fi
            else
                if [ "$1" = "down" ]; then
                    echo "no interface: client"
                else
                    sudo wg-quick up ~/.wg/client.conf >/dev/null 2>&1
                    echo
                    echo "interface: client created"
                    echo
                    sudo wg
                    echo
                fi
            fi
        '''))
        
    os.system('chmod +x server client')

    return dedent(f'''
        Shell scripts generated: ./server ./client\n
        {YELLOW}[Server]
        - External IP: {server_ip}
        - Internal IP: 10.0.0.1
        
        {CYAN}[Client]
        - Internal IP: 10.0.0.2\n{WHITE}
        🚨  {WHITE}{server_ip}{YELLOW}:{server_port}/udp{WHITE} should be reachable from {CYAN}client\n
        {WHITE}Handshake:
        {YELLOW}server $ ./server
        {CYAN}client $ ./client\n
        {WHITE}cURL test:
        {YELLOW}server $ python -m http.server
        {CYAN}client $ curl 10.0.0.1:8000
        {CYAN}client $ python -m http.server
        {YELLOW}server $ curl 10.0.0.2:8000\n
        {WHITE}Status check:
        {YELLOW}server $ ./server
        {CYAN}client $ ./client\n
        {WHITE}Disconnect:
        {CYAN}server $ ./server down
        {YELLOW}client $ ./client down
    ''')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(dedent(f'''
            Usage: {YELLOW}python3 wireguard.py SERVER_IP_OR_DOMAIN [PORT]{WHITE}

            Examples:
            {YELLOW}python3 wireguard.py 192.168.0.2
            python3 wireguard.py wg.yauk.tv 12345{WHITE} 
        '''))
    else:
        print(generate_config(sys.argv[1]))