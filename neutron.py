__author__ = 'Denis'

from hydra import *
from api import *

keystoneURL = 'http://10.0.2.15:5000'
credentials =   {
                    "auth": {
                        "tenantName": "demo",
                        "passwordCredentials": {
                            "username": "admin",
                            "password": "openstack"
                        }
                    }
                }

auth = {'usr': 'denis', 'pwd': 'warped', 'inst': '127.0.1.1'}


if __name__ == '__main__':
    api = API(keystoneURL, credentials)
    hydra = Hydra(auth)
    hosts = []



    l = api.neutron.listSubnets()
    for i in l:
        if i['name'] == 'private-subnet':

            start = i['allocation_pools'][0]['start']
            end = i['allocation_pools'][0]['end']
            print start, end

    for i in range(int(start.split('.')[3]), int(end.split('.')[3])+1):
        hosts.append('.'.join(start.split('.')[:-1])+'.'+str(i))

    #for i in range(int(len(hosts)/10)):
    #    hh = hosts[i*10:(i+1)*10]
    #    hydra.init_processes('ping', hh)
    #    hydra.stream(5)
    hydra.init_processes('ping', ['10.0.0.0', '10.0.0.15'])
    hydra.stream(25)
