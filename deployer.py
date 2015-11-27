#!/home/liqin/Works/python3.5Env/bin/python3

import os
import sys
from optparse import OptionParser
import json
import paramiko
import threading

__author__ = 'liqin'


def main():
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage, version='%prog 1.0')
    parser.add_option('-e', '--env', dest='env_config', help='config file of environment')

    options, args = parser.parse_args()
    if not options.env_config:
        parser.print_help()
        return 1

    env_file = os.path.join(os.path.abspath('.'), options.env_config)

    try:
        with open(env_file) as json_env_file:
            env_cfg = json.load(json_env_file)
    except Exception as e:
        parser.error('%s' % e)

    # set environment path to cfg
    env_cfg['base_path'] = os.path.split(env_file)[0]

    # start to deploy environment
    try:
        for d in env_cfg['deploy']:
            deploy_file = os.path.join(env_cfg['base_path'], d)
            deploy(env_cfg, deploy_file)
    except Exception as e:
        parser.error('%s' % e)

    return 0


def deploy(env_cfg, deploy_file):
    try:
        with open(deploy_file) as json_env_file:
            deploy_cfg = json.load(json_env_file)
    except Exception as e:
        raise e

    deploy_cfg['base_path'] = os.path.split(deploy_file)[0]

    t_group = []
    for s in deploy_cfg['servers']:

        for svr in env_cfg['servers']:
            if svr['name'] == s:
                break

        if 'sshKey' in svr:
            svr['sshKey'] = os.path.join(env_cfg['base_path'], svr['sshKey'])

        t = threading.Thread(target=deployOnServer, args=(svr, deploy_cfg))
        t.start()

        t_group.append(t)

    for t in t_group:
        t.join()


def deployOnServer(svr, deploy_cfg):
    # connect to server
    ssh_fd = None
    if 'password' in svr:
        ssh_fd = ssh_connect(svr['host'], svr['user'], port=svr['port'], password=svr['password'])
    elif 'sshKey' in svr:
        ssh_fd = ssh_connect(svr['host'], svr['user'], port=svr['port'], key=svr['sshKey'])

    if ssh_fd:
        print('connect to server %s:%s' % (svr['host'], svr['port']))
        try:
            sftpd = sftp_open(ssh_fd)
            if sftpd:
                for file in deploy_cfg['files']:

                    if not file['upload']:
                        continue
                    # upload file
                    try:
                        print('start to upload file %s' % file['name'])
                        f = sftp_put(sftpd, os.path.join(deploy_cfg['base_path'], file['name']),
                                     os.path.join(deploy_cfg['remotePath'], file['name']),
                                     callback=sfpt_put_progress)
                        print('\nupload file %s successfully' % f)
                    except Exception as e:
                        print("sftp error: %s" % e)
                        continue

                sftp_close(sftpd)
        except Exception as e:
            print("ssh error: %s" % e)
        finally:
            ssh_close(ssh_fd)


def ssh_connect(host, username, password=None, port=paramiko.config.SSH_PORT, key=None):
    try:
        _ssh_fd = paramiko.SSHClient()

        _ssh_fd.load_system_host_keys()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if key:
            _ssh_key = paramiko.RSAKey.from_private_key_file(key)
            _ssh_fd.connect(host, port, username=username, pkey=_ssh_key)
        elif password:
            _ssh_fd.connect(host, port, username=username, password=password)
        else:
            exit()

    except Exception as e:

        print('ssh %s@%s: %s' % (username, host, e))
        exit()

    return _ssh_fd


def ssh_close(ssh_fd):
    ssh_fd.close()


def sftp_open(ssh_fd):
    return ssh_fd.open_sftp()


def sftp_put(sftp_fd, put_from_path, put_to_path, callback=None):
    return sftp_fd.put(put_from_path, put_to_path, callback=callback)


def sftp_get(sftp_fd, get_from_path, get_to_path):
    return sftp_fd.get(get_from_path, get_to_path)


def sftp_close(sftp_fd):
    sftp_fd.close()


def sfpt_put_progress(transferred, toBeTransferred):
    percent = int(100 * (transferred / toBeTransferred))
    sys.stdout.write('\ruploading:{0}, {1}%'.format(transferred, percent))
    sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(main())
