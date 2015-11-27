#!/usr/bin/python3

import sys
from pymongo import MongoClient
from optparse import OptionParser
import datetime
import time
import json

__author__ = 'liqin'


def main():
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage, version='%prog 1.0')
    parser.add_option('-a', '--hosts', dest='hosts', help='mongodb hosts address: host1:port[, host2:port ...]')
    parser.add_option('-d', '--database', dest='db', help='db name')

    options, args = parser.parse_args()
    if not options.hosts or not options.db:
        parser.print_help()
        return 1

    hosts = options.hosts.split(',')
    print(hosts)

    client = MongoClient(hosts)

    print(options.db)
    # AddWorkerRoles(client, options.db)

    return 0


def AddWorkerRoles(db_client, db_name):
    worker_roles = db_client[db_name]['worker.role']

    count = 0
    roles = ['设计师', '工长', '水电工', '泥工', '木工', '漆工', '特工', '保洁']
    roles_craft = [['C-001', 'C-002', 'C-003'], ['C-001', 'C-002', 'C-004'], ['C-005', 'C-006', 'C-007'],
                   ['C-008', 'C-009', 'C-010', 'C-011'], ['C-012', 'C-013', 'C-014', 'C-015'],
                   ['C-016', 'C-017', 'C-018', 'C-019'],
                   ['C-006', 'C-007', 'C-020', 'C-014', 'C-021', 'C-022', 'C-011', 'C-023'],
                   ['C-024', 'C-025', 'C-026']]

    for role in roles:
        count += 1

        id = 'R-%03d' % (count)
        print(id, role)

        role_doc = {'id': '', 'name': '', 'crafts': []}
        role_doc['id'] = id
        role_doc['name'] = role
        role_doc['crafts'] = roles_craft[count - 1]

        worker_roles.insert_one(role_doc)

    print('%s' % worker_roles.count())

    worker_crafs = db_client[db_name]['worker.craft']
    crafts = ['家装', '工装', '软装', '局部装修', '改水电', '安灯/挂件', '安洁具', '找平', '贴瓷砖', '砌墙', '做防水', '吊顶', '做家具',
              '安家具', '安门',
              '乳胶漆', '硅藻泥', '木器漆', '真石漆', '安窗帘', '美缝', '贴墙纸', '铝扣板吊顶', '开荒', '深度保洁', '日常保洁']

    count = 0
    for craft in crafts:
        count += 1

        id = 'C-%03d' % (count)
        print(id, craft)

        craft_doc = {'id': '', 'name': ''}
        craft_doc['id'] = id
        craft_doc['name'] = craft

        worker_crafs.insert_one(craft_doc)

if __name__ == '__main__':
    sys.exit(main())
