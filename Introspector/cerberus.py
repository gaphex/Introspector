__author__ = 'denisantyukhov'

import sqlite3

class Cerberus:

    def __init__(self):
        self.db = 'database/dumps.db'
        self.conn = ''
        self.curs = ''
        self.tar = ''

    def connect_to_SQL(self, path=None):
        if path:
            self.db = path

        self.conn = sqlite3.connect(self.db)
        self.curs = self.conn.cursor()
        self.curs.execute("CREATE TABLE IF NOT EXISTS tcpdump (timestamp text, source text, destination text, flags text, seq text, ack text, win text, length text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS traceroute (timestamp text, n text, target text, hop text, p1 text, p2 text, p3 text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS ping (timestamp text, source text, traffic text, icmp_seq text, ttl text, time text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS iproute (timestamp text, target text, route text)")
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
            if item.__class__.__name__ == 'IPRoute':
                n += 1
                self.curs.execute("insert into iproute (timestamp, target, route) values(?, ?, ?)", (item.timestamp, item.target, str(item.route)))

        self.conn.commit()
        print 'Successfully committed', n, 'datagrams'
        print '-----------------------------------------------------------'
        print ''
        print ''

