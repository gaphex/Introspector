__author__ = 'denisantyukhov'

import time
import paramiko
import datetime

from cerberus import *
import multiprocessing as mp
from multiprocessing import Queue
from parser import Parser


class Hydra:

    def __init__(self, auth):
        self.bufs = []
        self.stacks = []
        self.parser = Parser()
        self.processes = []
        self.cerberus = None
        self.ssh_auth = auth
        self.streaming = False
        self.init_resources()

    @staticmethod
    def connect_to_box(host, port, username, password, timeout=3):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host, port=port, username=username, password=password, timeout=timeout)
        except Exception as e:
            print 'Could not connect to box: encountered exception', e
            print ''
            return None
        return client

    @staticmethod
    def get_timestamp():
        return datetime.datetime.now()

    def execute(self, auth, cmd, i):

        host = auth['host']
        usr = auth['usr']
        pwd = auth['pwd']
        port = auth['port']

        client = self.connect_to_box(host, port, usr, pwd)
        try:
            tr = client.get_transport()
            channel = tr.open_session()
        except Exception as e:
            channel = None
            print e

        try:
            com = cmd
            self.commands.put(com)
            channel.exec_command(com)
            print i, ': executing', com, 'on host', host
        except Exception as e:
            print 'could not execute on host', host, 'caught', e

        try:
            while not channel.exit_status_ready():
                r = channel.recv(4096)
                self.stacks[i].put(r)
                # print r

            print 'received exit code'
            return 0

        except Exception as e:
            print 'caught exception', e, 'closing channel...'
            channel.close()

    def start_streaming(self):

        for i, p in enumerate(self.processes):
            print '---- starting process #', i, '----'
            p.start()
        self.streaming = True

    def stop_streaming(self):
        for i, p in enumerate(self.processes):
            print '---- terminating process #', i, '----'
            p.terminate()
        self.streaming = False

    def wait(self, span):
        n = 5
        ts = span/n
        for i in range(n):
            finished = 0
            time.sleep(ts)
            for process in self.processes:
                if process.is_alive() == False:
                    finished += 1
            if finished == len(self.processes):
                return 0
        self.stop_streaming()

    def tcpdump(self, i, target):
        cmd = 'sudo tcpdump host ' + target + """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }' """
        self.execute(self.ssh_auth, cmd, i) # host '+target

    def ping(self, i, target):
        cmd = "sudo ping " + target + """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }' """
        self.execute(self.ssh_auth, cmd, i)

    def iproute(self, i, target):
        cmd = "sudo ip route get " + target + """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }' """
        self.execute(self.ssh_auth, cmd, i)

    def fping(self, i, target):
        if ':' in target:
            cmd = "sudo fping6 " + target + """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }'"""
        else:
            cmd = "sudo fping -g " + target + """ | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }'"""
        self.execute(self.ssh_auth, cmd, i)

    def traceroute(self, i, target):
        cmd = "sudo traceroute " + target + """ -T | awk '{ print strftime("\%Y-%m-%d %H:%M:%S\"), $0; fflush(); }'"""
        self.execute(self.ssh_auth, cmd, i)

    def init_resources(self):
        self.cerberus = Cerberus()
        self.commands = Queue()
        self.processes = []
        paramiko.util.log_to_file("log.log")

    def init_processes(self, action, hosts):

        if action == 'ping':
            tar = self.ping
        elif action == 'tcpdump':
            tar = self.tcpdump
        elif action == 'traceroute':
            tar = self.traceroute
        elif action == 'fping':
            tar = self.fping
        elif action == 'iproute':
            tar = self.iproute
        else:
            tar = None
            print 'invalid command, terminating'
            return 0

        if type(hosts) is not list:
            r = hosts
            hosts = list()
            hosts.append(r)

        self.processes = [mp.Process(target=tar, args=(i, host)) for i, host in enumerate(hosts)]
        self.stacks = [Queue() for process in self.processes]
        self.bufs = [list() for process in self.processes]

    def stream(self, span):

        commands = []
        self.start_streaming()
        self.wait(span)

        while not self.commands.empty():
            commands.append(self.commands.get(timeout=1))

        for i, stack in enumerate(self.stacks):
            while not stack.empty():
                tweet = stack.get(timeout=1)
                self.bufs[i].append(tweet)

        for i, buf in enumerate(self.bufs):
            print '------------------------------------------------'
            print 'buffer', i, commands[i]
            w = ''.join(buf).split('\n')
            if w:
                parsed = self.parser.parse_log(w[:-1], commands[i])
                if parsed:
                    try:
                        self.cerberus.commit_to_db(parsed)
                    except Exception as e:
                        print 'Could not commit datagrams to database:', e

