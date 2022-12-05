#!/usr/bin/python3

import yaml
import sys
from sys import argv


def read_states(vpn):
    with open('./vpns_states.yml', 'r') as file:
        vpn_dict = yaml.safe_load(file)
        state = int(vpn_dict.get(vpn))
    return state


def main():
    vpn = argv[1]
    return sys.exit(int(read_states(vpn)))


if __name__ == '__main__':

    main()
