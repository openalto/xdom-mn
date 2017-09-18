#!/usr/bin/env python

from mininet.cli import CLI
from mininet.log import info

def MCLI(**networks):
    prompt = 'crossdomain> '
    while True:
        cmd = raw_input(prompt)
        if cmd == 'quit':
            break
        if cmd == 'help':
            info('ls     list all available networks\n')
            info('<net>  switch the cli to <net>\n')
            info('quit   quit the cli and close the simulator\n')
            info('help   print this list\n')
        elif cmd == 'ls':
            info('\n'.join(sorted(networks.keys())))
            info('\n')
        elif cmd in networks.keys():
            CLI.prompt = '%s> ' % cmd
            info('***** Running CLI for %s *****\n' % cmd)
            net = networks[cmd]
            CLI(net)
        else:
            info('Unknown command: %s\n' % cmd)
