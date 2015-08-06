__author__ = 'Denis'

from auths import *
from hydra import *
from api import *
from manager import *
import pandas as pd
import ast
import sqlite3

def uniques(lst):
        return list(set(lst))


if __name__ == '__main__':
    api = API(keystoneURL, credentials)
    hydra = Hydra()
    jobs = []
    hosts = []
    subnets = []

    con = sqlite3.connect('database/driver_log.db')
    df = pd.read_sql('select * from subnet', con)

    for i in list(df['current']):
        datagram = ast.literal_eval(i)
        if datagram['ip_version'] == 4:
            subnets.append(datagram['cidr'])

    subnets.append('10.0.2.0/24')
    subnets = uniques(subnets)
    print subnets


    jobs = prepare_jobs('fping', subnets, auth)

    hydra.init_processes(jobs)
    hydra.run(15)


    con1 = sqlite3.connect('database/dumps.db')
    df = pd.read_sql("select * from ping where traffic like 'alive'", con1)
    hosts = [host for host in list(df['source'].drop_duplicates()) if host]
    print hosts







