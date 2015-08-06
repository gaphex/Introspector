__author__ = 'Denis'

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