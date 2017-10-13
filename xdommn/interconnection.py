#!/usr/bin/env python

from mininet.link import Link
from mininet.log import info
from mininet.net import Mininet


class InterConnection():
    """
    Maintain inter-connection links between neighbour domains.
    """

    def __init__(self):
        self.interconnections = []
        self.link = Link

    def addLink(self, node1, node2, port1=None, port2=None, cls=None,
                **params):
        # Accept node objects or names
        node1 = node1 if not isinstance(node1, basestring) else self[node1]
        node2 = node2 if not isinstance(node2, basestring) else self[node2]
        options = dict(params)
        # Port is optional
        if port1 is not None:
            options.setdefault('port1', port1)
        if port2 is not None:
            options.setdefault('port2', port2)
        # Set default MAC - this should probably be in Link
        options.setdefault('addr1', Mininet.randMac())
        options.setdefault('addr2', Mininet.randMac())
        cls = self.link if cls is None else cls
        link = cls(node1, node2, **options)
        self.interconnections.append(link)
        return link

    def stop(self):
        info('***** Stopping interconnections *****\n')
        for link in self.interconnections:
            info('.')
            link.stop()
        info('\n')
