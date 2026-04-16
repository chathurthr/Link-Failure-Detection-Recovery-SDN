from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpid_to_str
import pox.openflow.discovery as discovery
import networkx as nx

log = core.getLogger()

class LinkFailureController(EventMixin):
    def __init__(self):
        self.topology = nx.Graph()
        self.connections = {}

        core.openflow.addListeners(self)
        core.openflow_discovery.addListeners(self)

        log.info("Advanced Link Failure Controller Started")

    def _handle_ConnectionUp(self, event):
        self.connections[event.dpid] = event.connection
        self.topology.add_node(event.dpid)
        log.info("Switch Connected: %s", dpid_to_str(event.dpid))

    def _handle_LinkEvent(self, event):
        l = event.link

        if event.added:
            self.topology.add_edge(l.dpid1, l.dpid2)
            log.info("LINK UP: %s <-> %s", dpid_to_str(l.dpid1), dpid_to_str(l.dpid2))

        elif event.removed:
            if self.topology.has_edge(l.dpid1, l.dpid2):
                self.topology.remove_edge(l.dpid1, l.dpid2)

            log.warning("LINK FAILED: %s <-> %s", dpid_to_str(l.dpid1), dpid_to_str(l.dpid2))
            self.flush_flows()

    def flush_flows(self):
        for dpid, conn in self.connections.items():
            msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
            conn.send(msg)
        log.info("Flows Cleared for Recovery")

    def _handle_PacketIn(self, event):
        msg = of.ofp_packet_out(data=event.ofp)
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.in_port = event.port
        event.connection.send(msg)

def launch():
    discovery.launch()
    core.registerNew(LinkFailureController)
