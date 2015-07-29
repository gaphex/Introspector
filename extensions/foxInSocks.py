from neutron.api.v2 import base
from neutron.api import extensions
from neutron import manager
from neutron import wsgi
 

RESOURCE_ATTRIBUTE_MAP = {
    'foxinsocks': {
    'name': {'allow_post': True, 'allow_put': True,
                 'is_visible': True},
    'priority': {'allow_post': True, 'allow_put': True,
                 'is_visible': True},
    'credential': {'allow_post': True, 'allow_put': True,
                 'is_visible': True},
    'tenant_id': {'allow_post': True, 'allow_put': False,
                  'required_by_policy': True,
                  'validate': {'type:string': None},
                  'is_visible': True}
    }
}
 
class FoxInSocksController(wsgi.Controller):

    def index(self, request):
        return "Try to say this Mr. Knox, sir..."
 
class FoxInSocks(extensions.ExtensionDescriptor):
    # The name of this class should be the same as the file name
    # There are a couple of methods and their properties defined in the
    # parent class of this class, ExtensionDescriptor you can check them
    def __init__(self):
        pass

    @classmethod
    def get_name(cls):
        # You can coin a name for this extension
        return "Fox in socks"
 
    @classmethod
    def get_alias(cls):
        # This alias will be used by your core_plugin class to load
        # the extension
        return "foxinsock"
 
    @classmethod
    def get_description(cls):
        # A small description about this extension
        return "A quick brown fox jumped over a lazy dog"
 
    @classmethod
    def get_namespace(cls):
        # The XML namespace for this extension
        # but as we move on to use JSON over XML based request
        # this is not that important, correct me if I am wrong.
        return "http://whatdoesthesocksay.com"
 
    @classmethod
    def get_updated(cls):
        # Specify when was this extension last updated,
        # good for management when there are changes in the design
        return "2014-05-06T10:00:00-00:00"
 
    @classmethod
    def get_resources(cls):
	RESOURCE_NAME = 'foxinsock'
	COLLECTION_NAME = 'foxinsocks'

	exts = []
        plugin = manager.NeutronManager.get_plugin()

        controller = base.create_resource(COLLECTION_NAME, RESOURCE_NAME, plugin, RESOURCE_ATTRIBUTE_MAP.get(COLLECTION_NAME))
        ex = extensions.ResourceExtension(COLLECTION_NAME, controller)
        exts.append(ex)

        return exts


	#resources = []
        #resource = extensions.ResourceExtension('foxinsocks', FoxInSocksController())
        #resources.append(resource)
        #return resources