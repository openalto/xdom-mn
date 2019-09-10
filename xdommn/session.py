from mininet.log import info
from mininet.node import Host, RemoteController

from .crossdomain import (CrossDomainCLI, CrossDomainLink, CrossDomainMininet,
                          CrossDomainSwitch)
from .data import Data
from .utils import convert, getWholeName

class Session:

    def __init__(self, data):
        self.data = data
        self.net = None

    def start(self):
        self.net = start_session(self.data)

    def stop(self):
        info("*** Stopping network\n")
        if self.net:
            self.net.stop()

def start_session(data):
    domains_data = convert(data["domains"])
    links = set()
    hosts = dict()
    nodes = dict()
    switches = dict()
    controllers = dict()
    net = CrossDomainMininet(
        controller=RemoteController,
        switch=CrossDomainSwitch,
        link=CrossDomainLink,
        host=Host)

    for domain_name in sorted(domains_data.keys()):
        controller_name = domains_data[domain_name]["controller"]["name"]
        controller_ip = domains_data[domain_name]["controller"]["ip"]
        controller_port = domains_data[domain_name]["controller"]["port"]
        info("*** Connecting to Remote controller: %s \n" % (controller_name))
        c1 = net.addController(
            controller_name, ip=controller_ip, port=controller_port)
        controllers[controller_name] = c1
        Data().addSameName(controller_name)

        info("*** Adding switches to %s ***\n" % (domain_name))
        for switch_name in sorted(domains_data[domain_name]["switches"].keys()):
            try:
                ip = domains_data[domain_name]["switches"][switch_name]["ip"]
            except KeyError:
                ip = "127.0.0.1"
            switch_whole_name = getWholeName(domain_name, switch_name)
            print(switch_whole_name)
            backend_name = Data().getNextName(switch_whole_name, prefix='s')

            # Register the controller name of the switch in Data singleton
            Data().controllers[backend_name] = c1
            s1 = net.addSwitch(backend_name, ip=ip, protocols="OpenFlow13")
            switches[backend_name] = s1
            nodes[backend_name] = s1

        info("*** Adding hosts to %s ***\n" % (domain_name))
        for host_name in sorted(domains_data[domain_name]["hosts"].keys()):
            ip = domains_data[domain_name]["hosts"][host_name]["ip"]
            host_whole_name = getWholeName(domain_name, host_name)
            backend_name = Data().getNextName(host_whole_name, prefix='h')
            h1 = net.addHost(backend_name, **domains_data[domain_name]['hosts'][host_name])
            print(host_whole_name)
            hosts[backend_name] = h1
            nodes[backend_name] = h1

        info("*** Adding Links to %s ***\n" % (domain_name))
        for link in sorted(domains_data[domain_name]["links"]):
            node1 = Data().getBackEndName(getWholeName(domain_name, link[0]))
            node2 = Data().getBackEndName(getWholeName(domain_name, link[1]))
            node1 = nodes[node1]
            node2 = nodes[node2]
            link_args = link[2] if len(link) > 2 else {}
            l1 = net.addLink(node1, node2, **link_args)
            links.add(l1)

    interconnection_data = convert(data["interconnections"])
    for interconnection in sorted(interconnection_data):
        node1 = Data().getBackEndName(interconnection["node1"])
        node2 = Data().getBackEndName(interconnection["node2"])
        node1 = nodes[node1]
        node2 = nodes[node2]
        l1 = net.addLink(node1, node2)
        links.add(l1)

    info("*** Starting network\n")
    net.build()

    info("*** Starting Controllers ***\n")
    for controller in controllers.values():
        info("%s " % controller.name)
        controller.start()
    info("\n")

    for switch in switches.values():
        switch.start()

    return net

def start_with_cli(data, **args):
    "Create a network from semi-scratch with multiple controllers."
    net = start_session(data)

    info("*** Running CLI\n")
    CrossDomainCLI(net, **args)

    info("*** Stopping network\n")
    net.stop()
