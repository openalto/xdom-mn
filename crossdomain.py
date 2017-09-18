#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import Link
from mininet.log import setLogLevel, info

from util.multicli import MCLI

def crossdomain():
    """
    Example cross-domain netwroks:

            Domain 1:                 Domain 2:

                                      --- n2s2 --- n2h1
                                     /     |
    n1h1 --- n1s2 --- n1s1 ..... n2s1 --- c2
              \        /             \     |
               -- c1 --               --- n2s3 --- n2h2
    """
    net1 = Mininet()
    net2 = Mininet()

    info('*** Initiating net1 ***\n')
    c1 = RemoteController('c1', ip='172.17.0.2', port=6633)

    info('***** Adding switches for net1 *****\n')
    n1s1 = net1.addSwitch('n1s1', cls=OVSSwitch)
    n1s2 = net1.addSwitch('n1s2', cls=OVSSwitch)

    info('***** Adding hosts for net1 *****\n')
    n1h1 = net1.addHost('n1h1', ip='10.0.1.251')

    info('***** Adding links for net1 *****\n')
    net1.addLink(n1s1, n1s2)
    net1.addLink(n1h1, n1s2)

    info('***** Adding controller for net1 *****\n')
    net1.addController(c1)

    info('*** Initiating net2 ***')
    c2 = RemoteController('c2', ip='172.17.0.3', port=6634)

    info('***** Adding switches for net2 *****\n')
    n2s1 = net2.addSwitch('n2s1', cls=OVSSwitch)
    n2s2 = net2.addSwitch('n2s2', cls=OVSSwitch)
    n2s3 = net2.addSwitch('n2s3', cls=OVSSwitch)

    info('***** Adding hosts for net2 *****\n')
    n2h1 = net2.addHost('n2h1', ip='10.0.2.251')
    n2h2 = net2.addHost('n2h2', ip='10.0.2.252')

    info('***** Adding links for net2 *****\n')
    net2.addLink(n2s1, n2s2)
    net2.addLink(n2s1, n2s3)
    net2.addLink(n2h1, n2s2)
    net2.addLink(n2h2, n2s3)

    info('***** Adding controller for net1 *****\n')
    net2.addController(c2)

    info('*** Adding interconnection link ***\n')
    interconnections = []
    options = dict()
    options.setdefault( 'addr1', Mininet.randMac() )
    options.setdefault( 'addr2', Mininet.randMac() )
    link = Link( n1s1, n2s1, **options )
    interconnections.append( link )

    info('*** Starting net1 ***\n')
    net1.start()

    info('*** Starting net2 ***\n')
    net2.start()

    info('*** Running CLI for cross-domain network ***\n')
    MCLI(net1=net1, net2=net2)

    info('*** Stopping network ***\n')

    info('***** Stopping interconnections *****\n')
    for l in interconnections:
        l.stop()

    info('***** Stopping net1 *****\n')
    net1.stop()

    info('***** Stopping net2 *****\n')
    net2.stop()

if __name__ == '__main__':
    setLogLevel('info')
    crossdomain()
