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

    sudo pip install -e .

Usage
-----

.. code-block:: sh

   sudo ./bin/xdom-mn -c configs/sample.json


Execute command in cross-domain environment
-------

.. code-block::

   net1_h1 ping net2_h2

