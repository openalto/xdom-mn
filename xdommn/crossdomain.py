#!/usr/bin/env python2

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch, Node
from mininet.util import ipAdd, macColonHex

from .data import Data


class CrossDomainSwitch(OVSSwitch):
    """ Custom switch to connect to different controllers
    """
    def start( self, controllers ):
        "Start up a new OVS OpenFlow switch using ovs-vsctl"

        # Get controller from Data singleton
        new_controllers = [Data().controllers[self.name]]
        super(CrossDomainSwitch, self).start(new_controllers)

