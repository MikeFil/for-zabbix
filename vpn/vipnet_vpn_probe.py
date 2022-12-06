#!/usr/bin/python3

import paramiko
from time import sleep
import yaml


def read_config():
    with open('./config.yml', 'r') as file:
        config = yaml.safe_load(file)
        host = config.get('host')
        ip = host.get('ip')
        user = host.get('user')
        secret = host.get('password')
        port = host.get('port')
        vpns = config.get('tunnels')
    return ip, user, secret, port, vpns


def main():
    ip, user, secret, port, vpns = read_config()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=user, password=secret, port=port)

    while True:

        states = []

        for i in vpns:
            chan = client.invoke_shell()
            chan.send('iplir ping {} \n'.format(i))
            sleep(5)
            output = chan.recv(1000)
            if 'Connection successful' in str(output):
                states.append(1)
                print(i + ' : ' + '1')
            else:
                states.append(0)
                print(i + ' : ' + '0')

        vpns_states = dict(zip(vpns, states))

        with open('./vpns_states.yml', 'w') as file:
            yaml.dump(vpns_states, file)

        sleep(300)


if __name__ == '__main__':
    main()
