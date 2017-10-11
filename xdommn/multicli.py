#!/usr/bin/env python

import readline
import sys
from cmd import Cmd
from select import poll

from mininet.cli import CLI
from mininet.log import info


class CrossDomainCmd(Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None, **networks):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.intro = "A console to help controll crossdomain networks\n"
        self.prompt = "Cross Domain >"
        self.networks = networks["networks"]

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
        domain_name = arg.split()[0]
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
        args = arg.split()
        if len(args) < 2 or ":" not in args[0]:
            self.help_execute()
            return
        (domain, node_name) = args[0].split(':')
        new_args = [node_name]
        for parameter in args[1:]:
            if ":" in parameter:
                (tmp_domain_name, tmp_node_name) = parameter.split(':')
                tmp_node = self.networks[tmp_domain_name].get(tmp_node_name)
                new_args.append(tmp_node.IP())
            else:
                new_args.append(parameter)
        new_args = " ".join(new_args)
        MininetCustomCLI(mininet=self.networks[domain], command=new_args)

    def help_execute(self):
        print("Execute a command on a node")
        print("format: execute <domain_name:node_name> <command>")


class MininetCustomCLI(CLI):
    def __init__(self, mininet, stdin=sys.stdin, script=None, command=None):
        self.mn = mininet
        # Local variable bindings for py command
        self.locals = {'net': mininet}
        # Attempt to handle input
        self.stdin = stdin
        self.inPoller = poll()
        self.inPoller.register(stdin)
        self.inputFile = script
        Cmd.__init__(self)

        if self.inputFile:
            self.do_source(self.inputFile)
            return

        self.initReadline()
        if command is not None:
            self.default(command)


def MCLI(**networks):
    cmd = CrossDomainCmd(networks=networks)
    cmd.cmdloop()


if __name__ == '__main__':
    MCLI()
