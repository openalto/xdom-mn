#! /usr/bin/env python

from mininet.log import info
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController

from .interconnection import InterConnection
from .multicli import MCLI


def Start(data):
    domains_data = data["domains"]
    domains = {}
    controllers = {}
    nodes = {}
    interconnection = InterConnection()
    for name in domains_data.keys():
        domains[name] = Mininet()
    for name in domains_data.keys():
        info('*** Initiating ' + name + ' ***\n')
        controller_ip = domains_data[name]["controller"]["ip"]
        controller_name = domains_data[name]["controller"]["name"]
        controller_port = domains_data[name]["controller"]["port"]
        controller = RemoteController(
            controller_name, ip=controller_ip, port=controller_port)
        controllers[name] = controller

        info('*** Adding switches to ' + name + ' ***\n')
        for switch_name in domains_data[name]["switches"].keys():
            # switch_class = domains_data[name]["switches"][switch_name]["class"]
            switch_class = OVSSwitch
            nodes[switch_name] = domains[name].addSwitch(
                switch_name, switch_class)

        info('*** Adding hosts to ' + name + ' ***\n')
        for host_name in domains_data[name]["hosts"].keys():
            host_ip = domains_data[name]["hosts"][host_name]["ip"]
            nodes[host_name] = domains[name].addHost(host_name, ip=host_ip)

        info('*** Adding links to ' + name + ' ***\n')
        for link in domains_data[name]["links"]:
            domains[name].addLink(nodes[link[0]], nodes[link[1]])

        info('*** Adding controllers to ' + name + ' ***\n')
        domains[name].addController(controllers[name])

    for name in domains.keys():
        domains[name].start()

    info("*** Running CLI for cross-domain network ***\n")
    MCLI(**domains)

    info("*** Stopping network ***\n")
    interconnection.stop()

    for name in domains:
        info("*** Stopping " + name + " ***\n")
        domains[name].stop()
