__author__ = 'denisantyukhov'
from structures import *
import sqlite3


class Cerberus:

    def __init__(self):
        self.db = 'dumps.db'
        self.conn = ''
        self.curs = ''

    def connect_to_SQL(self):
        self.conn = sqlite3.connect(self.db)
        self.curs = self.conn.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS tcpdump (timestamp text, source text, destination text, flags text, seq text, ack text, win text, length text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS traceroute (timestamp text, n text, target text, hop text, p1 text, p2 text, p3 text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS ping (timestamp text, source text, traffic text, icmp_seq text, ttl text, time text)")
        self.conn.commit()

    def commit_to_db(self, lst):
        n = 0
        self.connect_to_SQL()
        print 'Connected to', self.db

        for item in lst:
            if item.__class__.__name__ == 'Trace':
                n += 1
                self.curs.execute("insert into traceroute (timestamp, n, target, hop, p1, p2, p3) values(?, ?, ?, ?, ?, ?, ?)", (item.timestamp, item.n, item.target, item.hop, item.p1, item.p2, item.p3))
            if item.__class__.__name__ == 'Ping':
                n += 1
                self.curs.execute("insert into ping (timestamp, source, traffic, icmp_seq, ttl, time) values(?, ?, ?, ?, ?, ?)", (item.timestamp, item.source, item.traffic, item.icmp_seq, item.ttl, item.time))
            if item.__class__.__name__ == 'TCPDump':
                n += 1
                self.curs.execute("insert into tcpdump (timestamp, source, destination, flags, seq, ack, win, length) values(?, ?, ?, ?, ?, ?, ?, ?)",(item.timestamp, item.source, item.destination, item.flag, item.seq, item.ack, item.win, item.length))

        self.conn.commit()
        print 'Successfully committed', n, 'datagrams'

    def parse_log(self, log, command):
        s = []
        t = ''

        if 'ping' in command:
            mode = 'ping'
        if 'tcpdump' in command:
            mode = 'tcpdump'
        if 'traceroute' in command:
            mode = 'trace'

        for datagram in log:
            w = datagram.split(' ')
            if mode == 'tcpdump':
                try:
                    tim = w[0]
                    src = w[w.index('IP') + 1]
                    dst = w[w.index('>') + 1]
                    flg = w[w.index('Flags') + 1]
                    ack = w[w.index('ack') + 1]
                    win = w[w.index('win') + 1]
                    length = w[w.index('length') + 1]
                    t = TCPDump(tim, src=src, dst=dst, flg=flg, ack=ack, win=win, length=length)
                except:
                    try:
                        tim = w[0]
                        src = w[w.index('IP')+1]
                        dst = ''.join(w[w.index('>')+1:])
                        t = TCPDump(tim, src=src, dst=dst)
                    except:
                        pass

                try:
                    seq = w[w.index('seq')+1]
                    t.seq = seq
                except:
                    pass

                finally:
                    s.append(t)

            if mode == 'ping':
                try:
                    traffic = w[w.index('bytes') - 1] + ' ' + w[w.index('bytes')]
                    src = w[w.index('from') + 1][:-1]
                    for j in w:
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = j
                        if j.startswith('icmp_seq'):
                            icmp = j.split('=')[1]
                        if j.startswith('ttl'):
                            ttl = j
                        if j.startswith('time'):
                            tim = j.split('=')[1]

                    t = Ping(timestamp, source=src, traffic=traffic, icmp_seq=icmp, ttl=ttl, tim=tim)

                except Exception as e:
                    pass
                finally:
                    if t:
                        s.append(t)

            if mode == 'trace':

                tar, hop, timestamp = '', '', ''
                n = 0
                p = []
                try:
                    for i, j in enumerate(w):
                        if j == 'traceroute' and w[i+1] == 'to':
                            tar = w[i+2]
                        if len(j.split(':')) == 3 and len(j) == 8:
                            timestamp = j
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
            self.commit_to_db(s)
