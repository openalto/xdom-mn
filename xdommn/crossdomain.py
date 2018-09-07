#!/usr/bin/env python2

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.log import error

from .data import Data

from itertools import chain

from threading import Thread
import zmq

class ZMQThread(Thread):
    def __init__(self, cli, zmq_ip, zmq_port):
        super(ZMQThread, self).__init__()
        self._cli = cli
        self._zmq_ip = zmq_ip
        self._zmq_port = zmq_port

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://%s:%d' % (self._zmq_ip, self._zmq_port))
        while True:
            msg = socket.recv()
            print(msg)
            socket.send(msg)
            self._cli.onecmd(msg)

class CrossDomainSwitch(OVSSwitch):
    """ Custom switch to connect to different controllers
    """
    def start( self, controllers=None):
        "Start up a new OVS OpenFlow switch using ovs-vsctl"

        # Get controller from Data singleton
        new_controllers = [Data().controllers[self.name]]
        super(CrossDomainSwitch, self).start(new_controllers)


class CrossDomainMininet(Mininet):
    def build( self ):
        super(CrossDomainMininet, self).build()
        self.frontEndName = {}
        for i in self.nameToNode.keys():
            self.frontEndName[Data().getFrontEndName(i)] = self.nameToNode[i]

    def __iter__(self):
        "return iterator over node names"
        for node in chain( self.hosts, self.switches, self.controllers ):
            name = Data().getFrontEndName(node.name)
            yield name

    def __getitem__(self, key):
        """net [ name ] operator: Return node(s) with given name(s)"""
        return self.frontEndName[key]

    def __contains__(self, item):
        "returns True if net contains named node"
        return item in self.frontEndName


class CrossDomainLink(TCLink):
    def __str__(self):
        (intf1, intf2) = (self.intf1.__str__(), self.intf2.__str__())
        (intf1, intf2) = [i.split('-') for i in (intf1, intf2)]
        (intf1, intf2) = [Data().getFrontEndName(i[0]) + "-" + i[1] for i in (intf1, intf2)]
        return '%s<->%s' % ( intf1, intf2 )


class CrossDomainCLI(CLI):
    def __init__(self, net, zmq_thread=True, zmq_ip="127.0.0.1", zmq_port=12333, **args):

        if zmq_thread:
            zmq_thread = ZMQThread(self, zmq_ip, zmq_port)
            zmq_thread.daemon = True
            zmq_thread.start()
            print("Start ZMQ on address: tcp://%s:%d" % (zmq_ip, zmq_port))

        CLI.__init__(self, mininet=net)

    prompt = "cross domain> "

    helpStr = (
        'You may also send a command to a node using:\n'
        '  <node> command {args}\n'
        'For example:\n'
        '  cross domain> h1 ifconfig\n'
        '\n'
        'The interpreter automatically substitutes IP addresses\n'
        'for node names when a node is the first arg, so commands\n'
        'like\n'
        '  cross domain> h2 ping h3\n'
        'should work.\n'
        '\n'
        'Some character-oriented interactive commands require\n'
        'noecho:\n'
        '  cross domain> noecho h2 vi foo.py\n'
        'However, starting up an xterm/gterm is generally better:\n'
        '  cross domain> xterm h2\n\n'
    )

    def default( self, line ):
        """Called on an input line when the command prefix is not recognized.
        Overridden to run shell commands when a node is the first CLI argument.
        Past the first CLI argument, node names are automatically replaced with
        corresponding IP addrs."""

        first, args, line = self.parseline( line )
        if first in self.mn:
            if not args:
                print "*** Enter a command for node: %s <cmd>" % first
                return
            node = self.mn[ first ]
            rest = args.split( ' ' )
            # Substitute IP addresses for node names in command
            # If updateIP() returns None, then use node name
            rest = [ self.mn[ arg ].defaultIntf().updateIP() or arg
                     if arg in self.mn else arg
                     for arg in rest ]
            rest = " ".join(rest)
            # Run cmd on node:
            node.sendCmd( rest )
            self.waitForNode( node )
        elif first == "name":
            rest = args.split( ' ' )
            backend_names = [ self.mn[front].name if front in self.mn else "NULL" for front in rest ]
            print ", ".join(backend_names)
        else:
            error( '*** Unknown command: %s\n' % line )
