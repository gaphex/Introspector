__author__ = 'Denis'
from structures import *
import datetime

def uniques(lst):
        return list(set(lst))

class Parser:
    def __init__(self):
        self.temp = ''

    @staticmethod
    def get_timestamp():
        return str(datetime.datetime.now())[:-7]

    def parse_log(self, log, command):              # will be reworked using regex expressions
        s = []
        t = None
        if 'fping' in command:
            mode = 'fping'
        elif 'ping' in command:
            mode = 'ping'
        elif 'tcpdump' in command:
            mode = 'tcpdump'
        elif 'traceroute' in command:
            mode = 'trace'
        elif 'fping' in command:
            mode = 'fping'
        elif 'ip route' in command:
            mode = 'iproute'
        else:
            print 'Parser does not support', command, 'terminating'

        for datagram in log:
            w = datagram.split(' ')

            if mode == 'tcpdump':
                timestamp, src, dst, flg, ack, win, seq, length = '', '', '', '', '', '', '', ''
                try:
                    for i, j in enumerate(w):
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = ' '.join(w[i-1:i+1])
                        if j == 'IP':
                            src = w[i+1]
                        if j == '>':
                            dst = w[i+1][:-1]
                        if j == 'Flags':
                            flg = w[i+1]
                        if j == 'seq':
                            seq = w[i+1]
                        if j == 'ack':
                            ack = w[i+1]
                        if j == 'win':
                            win = w[i+1][:-1]
                        if j == 'length':
                            length = w[i+1]

                    if timestamp:
                        t = TCPDump(timestamp, src=src, dst=dst, flg=flg, ack=ack, win=win, seq=seq, length=length)

                except Exception as e:
                    print e, w
                finally:
                    if t:
                        print t.__dict__
                        s.append(t)

            if mode == 'fping' and 'alive' in w:
                timestamp, src, traffic = '', '', ''
                try:
                    for i, j in enumerate(w):
                        if len(j.split('.')) == 4:
                            src = j
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = ' '.join(w[i-1:i+1])
                        traffic = 'alive'
                    t = Ping(timestamp, source=src, traffic=traffic)
                except Exception as e:
                    print e, w
                finally:
                    if t:
                        print t.__dict__
                        s.append(t)

            if mode == 'ping':
                timestamp, src, traffic, icmp, ttl, tim = '', '', '', '', '', ''
                try:
                    traffic = w[w.index('bytes') - 1] + ' ' + w[w.index('bytes')]
                    src = w[w.index('from') + 1][:-1]
                    for i, j in enumerate(w):
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = ' '.join(w[i-1:i+1])
                        if j.startswith('icmp_seq'):
                            icmp = j.split('=')[1]
                        if j.startswith('ttl'):
                            ttl = j
                        if j.startswith('time'):
                            tim = j.split('=')[1]

                    t = Ping(timestamp, source=src, traffic=traffic, icmp_seq=icmp, ttl=ttl, tim=tim)
                except Exception as e:
                    print e, w
                finally:
                    if t:
                        print t.__dict__
                        s.append(t)

            if mode == 'trace':
                n, hop, timestamp, p1, p2, p3 = '', '', '', '', '', ''
                n = 0
                p = []
                try:
                    for i, j in enumerate(w):
                        if j == 'traceroute':
                            self.temp = w[i+2]
                            break

                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = ' '.join(w[i-1:i+1])
                        if len(j.split('.')) == 4 and len(w[i+1].split('.')) == 4:
                            hop = j
                            n = w[i-2]
                        if j == 'ms':
                            p.append(w[i-1])

                    if len(p) == 3:
                        t = Trace(timestamp, n=n, target=self.temp, hop=hop, p1=p[0], p2=p[1], p3=p[2])
                    else:
                        t = Trace(self.get_timestamp(), n=0, target=self.temp, hop='127.0.1.1', p1=0, p2=0, p3=0)
                except Exception as e:
                    print e, w
                finally:
                    if t:
                        print t.__dict__
                        s.append(t)

            if mode == 'iproute':

                timestamp = ''
                route = []
                try:
                    for i, j in enumerate(w):
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = ' '.join(w[i-1:i+1])
                        if len(j.split('.')) == 4:
                            route.append(j)

                except Exception as e:
                    print e, w
                finally:
                    if route:
                        route.reverse()
                        t = IPRoute(timestamp, target=route[-1], route=route)
                        print t.__dict__
                        s.append(t)

        if len(s):
            s = uniques(s)
            return s
