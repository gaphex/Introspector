from neutron.plugins.ml2 import plugin
from oslo_log import log
LOG = log.getLogger(__name__)
 
class CoreExtensionPlugin(plugin.Ml2Plugin):
 
    # List out all the extensions your plugin supports
    # append your extensions to Ml2 supported extensions
    
    supported_extension_aliases = ["provider", "external-net", "binding",
                                    "quotas", "security-group", "agent",
                                    "dhcp_agent_scheduler",
                                    "multi-provider", "allowed-address-pairs",
                                    "extra_dhcp_opt", "subnet_allocation",
                                    "net-mtu", "vlan-transparent", 'foxinsock']

    #self.supported_extension_aliases.append('foxinsock')
 
    # for extending methods not defined in Ml2Plugin
    def create_foxinsock(self, context, foxinsock):
 	LOG.info(_("called create_foxinsock"))
        # this need not be called using "super" as this method is
        # specific to this class and not Ml2Plugin
        # foxinsock contains the data you need for your plugin
        # to process

    def update_foxinsock(self, context, id, foxinsock):
	LOG.info(_("called update_foxinsock"))
        # The id is the unique identifier to your entry, foxinsock is a
        # dictionary with values that needs to be updated with.
 
    def get_foxinsock(self, context, id, fields):
	LOG.info(_("called get_foxinsock"))
        # The id is the unique identifier to your entry.
        # fields are the columns that you wish to display.
 
    def get_foxinsocks(self, context, filters, fields):
	LOG.info(_("called get_foxinsocks"))
        # Note there is an extra 's'.
        # filters contains the column name with a value with which
        # you can return multiple row entries that matches the filter
        # fields are the columns that you wish to display.
 
    def delete_foxinsock(self, context, id):
	LOG.info(_("called delete_foxinsock"))
        # The id is the unique identifier that can be used to delete
        # the row entry of your database.
