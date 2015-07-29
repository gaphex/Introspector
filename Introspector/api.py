__author__ = 'denisantyukhov'

import requests

class API:
    def __init__(self, keystone, auth):
        self.keystoneURL = keystone
        self.credentials = auth
        self.keystone = self.Keystone(self)
        self.token_header = {}
        self.authorize()
        self.serviceURL = self.keystone.listServiceURL()
        self.neutron = self.Neutron(self)

    def authorize(self):
        authURL = self.keystoneURL + '/v2.0/tokens'
        r = requests.post(url=authURL, json=self.credentials)
        token = r.json()['access']['token']['id']
        self.token_header = {'X-Auth-Token': token}

    class Keystone(object):
        def __init__(self, master):
            self.master = master
            self.keystoneURL = self.master.keystoneURL

        def listServices(self):
            URL = self.keystoneURL + '/v3/services'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()

        def listEndpoints(self):
            URL = self.keystoneURL + '/v3/endpoints'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()

        def listServiceURL(self):
            name_id = {}
            name_url = {}
            r = self.listServices()
            for i in r['services']:
                name_id[i['id']] = i['name']

            r = self.listEndpoints()
            for i in r['endpoints']:
                if i['service_id'] in name_id:
                    if 'tenant_id' not in i['url']:
                        name_url[name_id[i['service_id']]] = i['url']
            return name_url

    class Neutron(object):
        def __init__(self, master):
            self.master = master
            self.neutronURL = master.serviceURL['neutron']

        def listPorts(self):
            URL = self.neutronURL + 'v2.0/ports'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['ports']

        def listNetworks(self):
            URL = self.neutronURL + 'v2.0/networks'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['networks']

        def listSubnets(self):
            URL = self.neutronURL + 'v2.0/subnets'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['subnets']

        def listRouters(self):
            URL = self.neutronURL + 'v2.0/routers'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['routers']

        def listExtensions(self):
            URL = self.neutronURL + 'v2.0/extensions'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['extensions']

        def callFox(self):
            URL = self.neutronURL + 'v2.0/foxinsocks'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()

        def showNetwork(self):
            URL = self.neutronURL + 'v2.0/networks'
            r = requests.get(url=URL, headers=self.master.token_header)
            return r.json()['networks']
