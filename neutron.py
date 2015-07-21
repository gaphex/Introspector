__author__ = 'Denis'

from hydra import *
from api import *

keystoneURL = 'http://10.0.2.15:5000'
credentials =   {
                    "auth": {
                        "tenantName": "demo",
                        "passwordCredentials": {
                            "username": "admin",
                            "password": "openstack"             # auths for API services
                        }
                    }
                }

auth = {'usr': 'denis', 'pwd': 'warped', 'inst': '127.0.0.1'}   # auths for SSH


if __name__ == '__main__':
    api = API(keystoneURL, credentials)
    hydra = Hydra(auth)
    cands = []
    hosts = []

    l = api.neutron.listSubnets()
    for i in l:                                                             # scanning allocation pools to add candidates for hosts
        if i['name'] == 'public-subnet' or i['name'] == 'private-subnet':
            start = i['allocation_pools'][0]['start']
            end = i['allocation_pools'][0]['end']
            s = int(start.split('.')[-1])
            e = int(end.split('.')[-1])

            print start, end, s, e
            for j in range(s, e+1):
                cands.append('.'.join(start.split('.')[:-1])+'.'+str(j))



    hydra.init_processes('ping', ['10.0.0.2', '10.0.2.15'])                 # executing ping to some hosts for 10 secs
    hydra.stream(10)
    hydra.init_processes('traceroute', ['10.0.0.2', '10.0.2.15'])           # executing traceroute to some hosts
    hydra.stream(10)
    hydra.init_processes('tcpdump', ['10.0.0.2', '10.0.2.15'])              # executing tcpdump on some hosts
    hydra.stream(10)
