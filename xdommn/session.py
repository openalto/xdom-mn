import collections

from mininet.cli import CLI
from mininet.log import info
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController

from .data import Data


def convert(data):
    """ Convert dict in unicode to dict in str.
    """
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


class CrossDomainSwitch(OVSSwitch):
    """ Custom switch to connect to different controllers
    """

    def start(self, controllers):
        """ Start the switch
        """
        super(CrossDomainSwitch, self).start(Data().controllers[self.name])


def Start(data):
    """ Start the session
    """
    mn = Mininet()
    domains_data = convert(data["domains"])
    nodes = {}
    for domain_name in domains_data.keys():
        info("*** Initiating " + domain_name + " ***\n")
        controller_ip = domains_data[domain_name]["controller"]["ip"]
        controller_name = domains_data[domain_name]["controller"]["name"]
        controller_port = domains_data[domain_name]["controller"]["port"]
        controller = RemoteController(
            controller_name, ip=controller_ip, port=controller_port)
        mn.addController(controller)

        info("*** Adding switches to " + domain_name + " ***\n")
        for switch_name in domains_data[domain_name]["switches"].keys():
            switch_whole_name = domain_name + ":" + switch_name

            # Register the <switch_name, controller> in Data().controllers
            Data().controllers[switch_whole_name] = controller

            # Add CrossDomainSwitch to mininet
            switch_class = CrossDomainSwitch
            nodes[switch_whole_name] = mn.addSwitch(switch_whole_name,
                                                    switch_class)

        info("*** Adding hosts to " + domain_name + " ***\n")
        for host_name in domains_data[domain_name]["hosts"].keys():
            host_whole_name = domain_name + ":" + host_name
            host_ip = domains_data[domain_name]["hosts"][host_name]["ip"]
            nodes[host_whole_name] = mn.addHost(host_whole_name, ip=host_ip)

    info("*** Adding interconnection between networks ***\n")
    interconnection_data = convert(data["interconnection"])
    for connection in interconnection_data:
        (node1, node2) = (connection["node1"], connection["node2"])
        info(node1 + " <-> " + node2)
        mn.addLink(node1, node2)
    info("\n")

    # Start mininet
    mn.start()

    # Use mininet shell
    CLI(mn)

    # Stop mininet
    info("*** Stopping mininet ***\n")
    mn.stop()
