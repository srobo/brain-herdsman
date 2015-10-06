Herdsman
========

Herdsman is a WAMP/HTTP client/server which is used as the primary low-level
interface for remotely communicating with the robot. It provides functionality
such as starting/stopping the user code, reading the logs, and providing a way
of communicating directly with the user code.

Installation
------------

.. code:: shell

    $ pip install .

Running
-------

.. code:: shell

    $ crossbar start &
    $ herdsman -s path/to/tablet/interface
