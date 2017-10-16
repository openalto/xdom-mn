#!/usr/bin/env python2

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch

from .data import Data


class CrossDomainSwitch(OVSSwitch):
    """ Custom switch to connect to different controllers
    """

    def start( self, controllers ):
        "Start up a new OVS OpenFlow switch using ovs-vsctl"

        # Get controller from Data singleton
        controllers = [Data().controllers[self.name]]

        self.hashname = Data().getNextName(self.name, prefix="s")
        if self.inNamespace:
            raise Exception(
                'OVS kernel switch does not work in a namespace' )
        int( self.dpid, 16 )  # DPID must be a hex string
        # Command to add interfaces
        intfs = ''.join( ' -- add-port %s %s' % ( self, intf ) +
                         self.intfOpts( intf )
                         for intf in self.intfList()
                         if self.ports[ intf ] and not intf.IP() )
        # Command to create controller entries
        clist = [ ( self.hashname + c.name, '%s:%s:%d' %
                    ( c.protocol, c.IP(), c.port ) )
                  for c in controllers ]
        if self.listenPort:
            clist.append( ( self.hashname + '-listen',
                            'ptcp:%s' % self.listenPort ) )
        ccmd = '-- --id=@%s create Controller target=\\"%s\\"'
        if self.reconnectms:
            ccmd += ' max_backoff=%d' % self.reconnectms
        cargs = ' '.join( ccmd % ( name, target )
                          for name, target in clist )
        # Controller ID list
        cids = ','.join( '@%s' % name for name, _target in clist )
        # Try to delete any existing bridges with the same name
        if not self.isOldOVS():
            cargs += ' -- --if-exists del-br %s' % self
        # One ovs-vsctl command to rule them all!
        self.vsctl( cargs +
                    ' -- add-br %s' % self +
                    ' -- set bridge %s controller=[%s]' % ( self, cids  ) +
                    self.bridgeOpts() +
                    intfs )
        # If necessary, restore TC config overwritten by OVS
        if not self.batch:
            for intf in self.intfList():
                self.TCReapply( intf )


class CrossDomainMininet(Mininet):
    def addLink( self, node1, node2, port1=None, port2=None,
                 cls=None, **params ):
        """"Add a link from node1 to node2
            node1: source node (or name)
            node2: dest node (or name)
            port1: source port (optional)
            port2: dest port (optional)
            cls: link class (optional)
            params: additional link params (optional)
            returns: link object"""
        # Accept node objects or names
        node1 = node1 if not isinstance( node1, basestring ) else self[ node1 ]
        node2 = node2 if not isinstance( node2, basestring ) else self[ node2 ]
        options = dict( params )
        # Port is optional
        if port1 is not None:
            options.setdefault( 'port1', port1 )
        if port2 is not None:
            options.setdefault( 'port2', port2 )
        # Set default MAC - this should probably be in Link
        options.setdefault( 'addr1', self.randMac() )
        options.setdefault( 'addr2', self.randMac() )
        cls = self.link if cls is None else cls
        link = cls( node1, node2, **options )
        self.links.append( link )
        return link
