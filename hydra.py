__author__ = 'denisantyukhov'

import time
import select
import paramiko

from cerberus import *
import multiprocessing as mp
from multiprocessing import Queue



class Hydra:

    def __init__(self, auth):
        self.bufs = []
        self.stacks = []
        self.processes = []
        self.usr = auth['usr']
        self.pwd = auth['pwd']
        self.inst = auth['inst']
        self.streaming = False
        self.init_resources()

    @staticmethod
    def connect_to_box(host, username, password, timeout=3):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(host, username=username, password=password, timeout=timeout)
        except Exception as e:
            print 'Could not connect to box: encountered exception', e
            print ''
            return None
        return client

    def execute(self, host, usr, pwd, cmd, i):

        client = self.connect_to_box(host, usr, pwd)
        tr = client.get_transport()
        channel = tr.open_session()

        com = cmd
        self.commands.put(com)
        channel.exec_command(com)
        print i, ': executing', com, 'on host', host

        try:
            while not channel.exit_status_ready():
                rl, wl, xl = select.select([channel], [], [], 0.0)
                r = 0
                if len(rl) > 0:
                    r = channel.recv(512)
                    self.stacks[i].put(r)
                    #print r
            print 'received exit code'

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
            #p.join(timeout=1)
            p.terminate()
        self.streaming = False

    def tcpdump(self, i, target):
        cmd = 'sudo tcpdump host ' + target
        self.execute(self.inst, self.usr, self.pwd, cmd, i) # host '+target

    def ping(self, i, target):
        cmd = "ping " + target + " | while read pong; do echo $(date): $pong; done"
        self.execute(self.inst, self.usr, self.pwd, cmd, i)

    def tracert(self, i, target):
        cmd = "traceroute " + target + " | while read pong; do echo $(date): $pong; done"
        self.execute(self.inst, self.usr, self.pwd, cmd, i)

    def init_resources(self):
        self.cerberus = Cerberus()
        self.commands = Queue()
        self.processes = []

    def init_processes(self, action, hosts):
        tar = ''
        if action == 'ping':
            tar = self.ping
        if action == 'dump':
            tar = self.tcpdump
        if action == 'traceroute':
            tar = self.tracert

        self.processes = [mp.Process(target=tar, args=(i, host)) for i, host in enumerate(hosts)]
        self.stacks = [Queue() for process in self.processes]
        self.bufs = [list() for process in self.processes]

    def stream(self, span):
        mb = []
        commands = []
        self.start_streaming()
        time.sleep(span)
        self.stop_streaming()

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
                self.cerberus.parse_log(w[:-1], commands[i])




