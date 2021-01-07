# Herdsman

**Herdsman is no longer used or maintained.** It has been replaced by
[astoria][].

[astoria]: https://github.com/srobo/astoria

Herdsman is a WAMP/HTTP client/server which was used as the primary
low-level interface for remotely communicating with the robot. It
provides functionality such as starting/stopping the user code, reading
the logs, and providing a way of communicating directly with the user
code.

## Installation

```console
$ pip install .
```

If you're not running Herdsman on SR kit, you'll need to use
[pyenv-dummy][] by setting `PYTHONPATH=/path/to/pyenv-dummy`. (At time
of writing, pyenv-dummy is outdated; you will need to move `sr/robot.py`
to `sr/robot/__init__.py`, and install [this
file](https://gist.github.com/sersorrel/8adb310fb542f19a28dcfef9aa47b9df)
at `sr/robot/power.py`.)

[pyenv-dummy]: https://github.com/srobo/pyenv-dummy

You will also need a set of webpages to serve, like
[tablet-interface][].

[tablet-interface]: https://github.com/srobo/tablet-interface

## Running

```console
$ herdsman -s /path/to/tablet-interface -u /path/to/robot.zip
```

If not running as root, you can pass `-p 8080` to avoid trying to listen
on port 80.

Several other options are available, see `herdsman --help`.
