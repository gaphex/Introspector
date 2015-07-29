__author__ = 'Denis'

from hydra import *
from api import *
from cerberus import *
import pandas as pd
import ast
import sqlite3
keystoneURL = 'http://10.0.2.15:5000'
credentials = {
    "auth": {
        "tenantName": "demo",
        "passwordCredentials": {
            "username": "admin",
            "password": "openstack"  # auths for API services
        }
    }
}

auth = {'usr': 'denis', 'pwd': 'warped', 'port': 22, 'host': '127.0.1.1'}  # auths for SSH

if __name__ == '__main__':
    api = API(keystoneURL, credentials)
    hydra = Hydra(auth)
    hosts = []
    ipv4_pools = []
    ipv6_pools = []

    con = sqlite3.connect('/opt/stack/neutron/neutron/plugins/ml2/drivers/inspector/inspector.db')
    df = pd.read_sql('select * from subnet', con)

    for j, i in enumerate(list(df['current'])):
        for pool in ast.literal_eval(i)['allocation_pools']:
            if ':' in pool['start']:
                if pool not in ipv6_pools:
                    ipv6_pools.append(pool)
            else:
                if pool not in ipv4_pools:
                    ipv4_pools.append(pool)

    ipv4_pools.append({'start': '10.0.2.0', 'end': '10.0.2.15'})

    for pool in ipv4_pools:
        target = pool['start'] + '/23'
        hydra.init_processes('fping', target)
        hydra.stream(5)


    con1 = sqlite3.connect('dumps.db')
    df = pd.read_sql("select * from ping where traffic like 'alive'", con1)
    hosts = [host for host in list(df['source'].drop_duplicates()) if host]

    for host in hosts:
        hydra.init_processes('tcpdump', host)
        hydra.stream(15)

    print hosts



