#!/home/liqin/python2.7Env/bin/python

import psutil
import sys
import yaml
from SocketServer import TCPServer

__author__ = 'liqin'


def main():

    host = "localhost"
    port = 9999
    addr = (host, port)

    #购置TCPServer对象，
    server = TCPServer(addr, MyBaseRequestHandlerr)

    #启动服务监听
    server.serve_forever()

    project = {'name': 'Silenthand Olleander',
                'race': 'Human',
                'traits': ['ONE_HAND', 'ONE_EYE']
                }

    with open('data.yaml', 'w') as outfile:
        yaml.dump(project, outfile, default_flow_style=False)

    with open('data.yaml', 'r') as f:
        x = yaml.load(f)
        print x

    return

    scputimes = psutil.cpu_times()
    print(scputimes.user)
    print(psutil.cpu_percent(interval=1))
    print(psutil.cpu_count())
    print(psutil.cpu_count(logical=False))
    print(psutil.virtual_memory())
    print(psutil.swap_memory())
    print(psutil.disk_partitions())

    sdiskusage = psutil.disk_usage('/')
    print(sdiskusage.total)

    print(psutil.disk_io_counters(perdisk=False))

    print(psutil.net_io_counters(pernic=True))

    print(len(psutil.net_connections()))
    print(psutil.net_if_addrs())
    print(psutil.net_if_stats())

    print(psutil.pids())

    for p in psutil.process_iter():
        print(p.name())


if __name__ == '__main__':
    sys.exit(main())
