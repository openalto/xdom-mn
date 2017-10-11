XDom-MN
=======

Mininet extensions for inter-domain simulation.

Features:

-  A CLI extension for multiple domain management.

TODOs:

-  An easy-to-use network template framework for inter-domain
   simulation.
-  A cluster deployer for large-scale test.

Prerequisites
-------------

You need to install mininet_ first.

.. _mininet: https://github.com/mininet/mininet

Installation
------------

.. code-block:: sh

    python setup.py install

Usage
-----

.. code-block:: sh

   sudo ./bin/xdom-mn -c configs/sample.json

In the shell
------------

.. code-block::

   help                   Show help documentations
   help <topic>           Show the usage of a topic
   ls                     Show all avaiable domains
   net <domain>           Choose a domain and connect to its mininet shell
   exit/quit              Exit the console
   execute <command>      run a command on the cross-domain environment

Example
-------

.. code-block::

   execute net1:n1h1 ping net2:n2h2

