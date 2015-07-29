'''
    for i in l:
        for j in i['allocation_pools']:
            sas.append(ipaddress.summarize_address_range(ipaddress.ip_address(j['start']),  ipaddress.ip_address(j['end'])))

    sas.append(ipaddress.summarize_address_range(ipaddress.ip_address(u'10.0.2.0'), ipaddress.ip_address(u'10.0.2.255')))

    for i in sas:
        for j in list(i):
            u = str(j)
            if ':' not in u:
                gg = []
                zz = u.split('/')
                if int(zz[1])>30:
                    u = str(zz[0]+'/30')

                gg.append(u)
                hydra.init_processes('fping', gg)              # executing tcpdump on some hosts
                hydra.stream(5) '''


for i in range(b1, e1):
        w = beg.split('.')
        u = '.'.join(w[:-1]) + '.' + str(i)
        hydra.init_processes('ping', u)
        hydra.stream(3)