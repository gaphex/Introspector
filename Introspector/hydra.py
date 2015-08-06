__author__ = 'denisantyukhov'

import time
import paramiko
from cerberus import *
from parser import Parser
import multiprocessing as mp
from structures import namedBuffer

class Hydra:

    def __init__(self):

        self.processes = []
        self.containers = []
        self.streaming = False
        self.parser = Parser()
        self.cerberus = Cerberus()
        paramiko.util.log_to_file("hydra.log")

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
            channel.exec_command(com)
            print i, ': executing', com, 'on host', host
        except Exception as e:
            print 'could not execute on host', host, 'caught', e

        try:

            while not channel.exit_status_ready():
                r = channel.recv(4096)
                self.containers[i].queue.put(r)
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
                if not process.is_alive():
                    finished += 1
            if finished == len(self.processes):
                return 0
        self.stop_streaming()

    def init_processes(self, jobs):

        self.processes = [mp.Process(target=self.execute, args=(job.auth, job.command, i)) for i, job in enumerate(jobs)]
        self.containers = [namedBuffer(name=job.command) for job in jobs]

    def run(self, span):
        if span < 5:
            span = 5
            
        self.start_streaming()
        self.wait(span)

        for i, buf in enumerate(self.containers):

            while not buf.queue.empty():
                datagram = buf.queue.get(timeout=1)
                buf.buffer.append(datagram)

        for i, buf in enumerate(self.containers):
            print '------------------------------------------------'
            print 'buffer', i, buf.name
            w = ''.join(buf.buffer).split('\n')
            if w:
                parsed = self.parser.parse_log(w, buf.name)
                if parsed:
                    try:
                        self.cerberus.commit_to_db(parsed)
                    except Exception as e:
                        print 'Could not commit datagrams to database:', e

