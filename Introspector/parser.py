__author__ = 'Denis'
from structures import *


def parse_log(log, command):              # will be reworked using regex expressions
    s = []
    t = ''

    if 'ping' in command:
        mode = 'ping'
    if 'tcpdump' in command:
        mode = 'tcpdump'
    if 'traceroute' in command:
        mode = 'trace'
    if 'fping' in command:
        mode = 'fping'

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

                t = TCPDump(timestamp, src=src, dst=dst, flg=flg, ack=ack, win=win, seq=seq, length=length)
                print t.__dict__

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

            n, tar, hop, timestamp, p1, p2, p3 = '', '', '', '', '', '', ''
            n = 0
            p = []

            if 'traceroute' in w:
                tar = w[w.index('traceroute')+2]

            try:
                for i, j in enumerate(w):

                    if len(j.split(':')) == 3 and len(j) == 8:
                        timestamp = ' '.join(w[i-1:i+1])
                    if len(j.split('.')) == 4 and len(w[i+1].split('.')) == 4:
                        hop = j
                        n = w[i-1]
                    if j == 'ms':
                        p.append(w[i-1])

                if len(p) == 3:
                    t = Trace(timestamp, n=n, target=tar, hop=hop, p1=p[0], p2=p[1], p3=p[2])

            except Exception as e:
                print e, w

            finally:
                if t:
                    print t.__dict__
                    s.append(t)

    if len(s):
        return s
