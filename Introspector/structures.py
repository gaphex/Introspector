__author__ = 'denisantyukhov'
from multiprocessing import Queue

class TCPDump:

    def __init__(self, tim, src=None, dst=None, flg=None, seq=None, ack=None, win=None, length=None):
        self.timestamp = tim
        self.source = src
        self.length = length
        self.destination = dst
        self.flag = flg
        self.seq = seq
        self.ack = ack
        self.win = win


class Ping:

    def __init__(self, timestamp, source=None, traffic=None, icmp_seq=None, ttl=None, tim=None):
        self.timestamp = timestamp
        self.source = source
        self.traffic = traffic
        self.icmp_seq = icmp_seq
        self.ttl = ttl
        self.time = tim


class Trace:

    def __init__(self, timestamp, target=None, n=None, hop=None, p1=None, p2=None, p3=None):
        self.timestamp = timestamp
        self.target = target
        self.n = n
        self.hop = hop
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


class IPRoute:

    def __init__(self, timestamp, target=None, route=None):
        self.timestamp = timestamp
        self.target = target
        self.route = route


class namedBuffer:

    def __init__(self, name=None):
        self.name = name
        self.queue = Queue()
        self.buffer = list()


class Job:

    def __init__(self, auth, command):
        self.auth = auth
        self.command = command



