# Herdsman

Herdsman is a WAMP/HTTP client/server which is used as the primary
low-level interface for remotely communicating with the robot. It
provides functionality such as starting/stopping the user code, reading
the logs, and providing a way of communicating directly with the user
code.

## Installation

```console
$ pip install .
```

## Running

```console
$ herdsman -s /path/to/tablet-interface -u /path/to/robot.zip
```

If not running as root, you can pass `-p 8080` to avoid trying to listen
on port 80.

Several other options are available, see `herdsman --help`.
