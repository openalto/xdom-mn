from mininet.log import info
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController, Host
from mininet.link import OVSLink

from .data import Data

from .utils import convert, getWholeName
from .crossdomain import CrossDomainSwitch, CrossDomainCLI, CrossDomainMininet, CrossDomainLink


def Start(data):
    "Create a network from semi-scratch with multiple controllers."

    domains_data = convert(data["domains"])
    links = set()
    hosts = dict()
    nodes = dict()
    switches = dict()
    controllers = dict()
    net = CrossDomainMininet(controller=RemoteController, switch=CrossDomainSwitch, link=CrossDomainLink, host=Host)

    for domain_name in domains_data.keys():
        controller_name = domains_data[domain_name]["controller"]["name"]
        controller_ip = domains_data[domain_name]["controller"]["ip"]
        controller_port = domains_data[domain_name]["controller"]["port"]
        info("*** Connecting to Remote controller: %s \n" % (controller_name))
        c1 = net.addController(controller_name, ip=controller_ip, port=controller_port)
        controllers[controller_name] = c1
        Data().addSameName(controller_name)

        info("*** Adding switches to %s ***\n" % (domain_name))
        for switch_name in domains_data[domain_name]["switches"].keys():
            switch_whole_name = getWholeName(domain_name, switch_name)
            backend_name = Data().getNextName(switch_whole_name, prefix='s')

            # Register the controller name of the switch in Data singleton
            Data().controllers[backend_name] = c1
            s1 = net.addSwitch(backend_name)
            switches[backend_name] = s1
            nodes[backend_name] = s1

        info("*** Adding hosts to %s ***\n" % (domain_name))
        for host_name in domains_data[domain_name]["hosts"].keys():
            host_whole_name = getWholeName(domain_name, host_name)
            backend_name = Data().getNextName(host_whole_name, prefix='h')
            h1 = net.addHost(backend_name)
            hosts[backend_name] = h1
            nodes[backend_name] = h1

        info("*** Adding Links to %s ***\n" % (domain_name))
        for link in domains_data[domain_name]["links"]:
            node1 = Data().getBackEndName(getWholeName(domain_name, link[0]))
            node2 = Data().getBackEndName(getWholeName(domain_name, link[1]))
            node1 = nodes[node1]
            node2 = nodes[node2]
            l1 = net.addLink(node1, node2)
            links.add(l1)

    interconnection_data = convert(data["interconnections"])
    for interconnection in interconnection_data:
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

    info("*** Running CLI\n")
    CrossDomainCLI(net)

    info("*** Stopping network\n")
    net.stop()
