#!/usr/bin/env python

import readline
from cmd import Cmd

from mininet.cli import CLI
from mininet.log import info


class CrossDomainCmd(Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None, **networks):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.intro = "A console to help controll crossdomain networks\n"
        self.prompt = "Cross Domain >"
        self.networks = networks

    def do_ls(self, arg):
        print('\n'.join(sorted(self.networks.keys())))
        print('\n')

    def help_ls(self):
        print("List all available networks\n")

    def do_exit(self, arg):
        return True

    def help_exit(self):
        print("Exit the console")

    do_quit = do_exit

    help_quit = help_exit

    do_EOF = do_exit

    help_EOF = help_exit

    def do_net(self, arg):
        domain_name = arg.split(' ')[0]
        if domain_name in self.networks.keys():
            print('***** Running CLI for %s *****\n' % domain_name)
            net = self.networks[domain_name]
            CLI(net)
        else:
            print("***** Cannot find domain named \"" + domain_name +
                  "\" *****")

    def help_net(self):
        print("Choose a domain and connect its mininet shell")
        print("format: net <domain name>")

    def do_execute(self, arg):
        # TODO: do some magic
        pass

    def help_execute(self):
        print("Execute a command on a node")
        print("format: execute <domain_name:node_name> <command>")


def MCLI(**networks):
    cmd = CrossDomainCmd(networks)
    cmd.cmdloop()


if __name__ == '__main__':
    MCLI()
