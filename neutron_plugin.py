import sqlite3
import datetime
from oslo_log import log
from neutron.plugins.ml2 import driver_api as api

LOG = log.getLogger('Introspector')


class Inspector(api.MechanismDriver):

    def initialize(self):
        self.db = 'database/driver_log.db'
        self.conn = sqlite3.connect(self.db)
        self.curs = self.conn.cursor()

        self.curs.execute("CREATE TABLE IF NOT EXISTS network (timestamp text, method_name text, current text, original text, segments text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS subnet (timestamp text, method_name text, current text, original text)")
        self.curs.execute("CREATE TABLE IF NOT EXISTS port (timestamp text, method_name text, current text, original text, host text, original_host text, vif_type text, original_vif_type text, vif_details text, original_vif_details text, levels text, original_levels text, network text, segments_to_bind text)")

        self.conn.commit()
        LOG.info(_("Inspector has connected to it's database"))

    def _log_network_call(self, method_name, context):
        LOG.info(_("%(method)s called with network settings %(current)s "
                   "(original settings %(original)s) and "
                   "network segments %(segments)s"),
                 {'method': method_name,
                  'current': context.current,
                  'original': context.original,
                  'segments': context.network_segments})
        self.curs.execute("insert into network (timestamp, method_name, current, original, segments) values(?, ?, ?, ?, ?)", (self.get_timestamp(), str(method_name), str(context.current), str(context.original), str(context.network_segments)))
        self.conn.commit()

    def create_network_precommit(self, context):
        self._log_network_call("create_network_precommit", context)

    def create_network_postcommit(self, context):
        self._log_network_call("create_network_postcommit", context)

    def update_network_precommit(self, context):
        self._log_network_call("update_network_precommit", context)

    def update_network_postcommit(self, context):
        self._log_network_call("update_network_postcommit", context)

    def delete_network_precommit(self, context):
        self._log_network_call("delete_network_precommit", context)

    def delete_network_postcommit(self, context):
        self._log_network_call("delete_network_postcommit", context)

    def _log_subnet_call(self, method_name, context):
        LOG.info(_("%(method)s called with subnet settings %(current)s "
                   "(original settings %(original)s)"),
                 {'method': method_name,
                  'current': context.current,
                  'original': context.original})
        self.curs.execute("insert into subnet (timestamp, method_name, current, original) values(?, ?, ?, ?)", (self.get_timestamp(), str(method_name), str(context.current), str(context.original)))
        self.conn.commit()

    def create_subnet_precommit(self, context):
        self._log_subnet_call("create_subnet_precommit", context)

    def create_subnet_postcommit(self, context):
        self._log_subnet_call("create_subnet_postcommit", context)

    def update_subnet_precommit(self, context):
        self._log_subnet_call("update_subnet_precommit", context)

    def update_subnet_postcommit(self, context):
        self._log_subnet_call("update_subnet_postcommit", context)

    def delete_subnet_precommit(self, context):
        self._log_subnet_call("delete_subnet_precommit", context)

    def delete_subnet_postcommit(self, context):
        self._log_subnet_call("delete_subnet_postcommit", context)

    def _log_port_call(self, method_name, context):
        network_context = context.network
        LOG.info(_("%(method)s called with port settings %(current)s "
                   "(original settings %(original)s) "
                   "host %(host)s "
                   "(original host %(original_host)s) "
                   "vif type %(vif_type)s "
                   "(original vif type %(original_vif_type)s) "
                   "vif details %(vif_details)s "
                   "(original vif details %(original_vif_details)s) "
                   "binding levels %(levels)s "
                   "(original binding levels %(original_levels)s) "
                   "on network %(network)s "
                   "with segments to bind %(segments_to_bind)s"),
                 {'method': method_name,
                  'current': context.current,
                  'original': context.original,
                  'host': context.host,
                  'original_host': context.original_host,
                  'vif_type': context.vif_type,
                  'original_vif_type': context.original_vif_type,
                  'vif_details': context.vif_details,
                  'original_vif_details': context.original_vif_details,
                  'levels': context.binding_levels,
                  'original_levels': context.original_binding_levels,
                  'network': network_context.current,
                  'segments_to_bind': context.segments_to_bind})
        self.curs.execute("insert into port (timestamp, method_name, current, original, host, original_host, vif_type, original_vif_type, vif_details, original_vif_details, levels, original_levels, network, segments_to_bind) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.get_timestamp(), str(method_name), str(context.current), str(context.original), str(context.host), str(context.original_host), str(context.vif_type), str(context.original_vif_type), str(context.vif_details), str(context.original_vif_details), str(context.binding_levels), str(context.original_binding_levels), str(network_context.current), str(context.segments_to_bind)))
        self.conn.commit()

    def create_port_precommit(self, context):
        self._log_port_call("create_port_precommit", context)

    def create_port_postcommit(self, context):
        self._log_port_call("create_port_postcommit", context)

    def update_port_precommit(self, context):
        self._log_port_call("update_port_precommit", context)

    def update_port_postcommit(self, context):
        self._log_port_call("update_port_postcommit", context)

    def delete_port_precommit(self, context):
        self._log_port_call("delete_port_precommit", context)

    def delete_port_postcommit(self, context):
        self._log_port_call("delete_port_postcommit", context)

    def bind_port(self, context):
        self._log_port_call("bind_port", context)
