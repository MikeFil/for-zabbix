#!/usr/bin/python3

from sys import argv
from pysnmp.entity.rfc3413.oneliner import cmdgen


class Device:

    def __init__(self, ip, community=community, port=161):
        self.ip = ip
        self.community = community
        self.port = port
        self.oid = '1.3.6.1.4.1.4413.1.1.1.1.4.9.0'

    def get_snmp(self):

        try:
            generator = cmdgen.CommandGenerator()
            comm_data = cmdgen.CommunityData('mes', self.community, 1)  # 1 means version SNMP v2c
            transport = cmdgen.UdpTransportTarget((self.ip, self.port))
            real_fun = getattr(generator, 'getCmd')
            result = real_fun(comm_data, transport, self.oid)
            data = str(str(result[-1][-1]).split(','))
            data = data.split(') ')

            return data

        except Exception as ex:
            print(f"Unexpected error: {ex}")

    def get_5sec_cpu_util(self):
        data = self.get_snmp()
        cpu_util = data[0]
        start = cpu_util.find('( ')
        cpu_util = cpu_util[start + 2:]
        end = cpu_util.find('.')
        cpu_util = cpu_util[:end]
        return cpu_util

    def get_60sec_cpu_util(self):
        data = self.get_snmp()
        cpu_util = data[1]
        start = cpu_util.find('( ')
        end = cpu_util.find('.')
        cpu_util = cpu_util[start + 2:end]
        return cpu_util

    def get_300sec_cpu_util(self):
        data = self.get_snmp()
        cpu_util = data[2]
        start = cpu_util.find('( ')
        end = cpu_util.find('.')
        cpu_util = cpu_util[start + 2:end]
        return cpu_util


if __name__ == "__main__":
    ip = argv[1]
    time = argv[2]
    community = argv[3]
    device = Device(ip, community)

    if time == '5':
        Print(int(device.get_5sec_cpu_util()))
    elif time == '60':
        Print(int(device.get_60sec_cpu_util()))
    elif time == '300':
        Print(int(device.get_300sec_cpu_util()))
