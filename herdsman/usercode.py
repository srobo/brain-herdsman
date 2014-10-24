import os 
import json
import shutil
from subprocess import Popen, call, check_output
import sys
import tarfile
import tempfile
import time
from twisted.internet import protocol
from twisted.internet import reactor
import zipfile

MODE_DEV = "dev"
MODE_COMP = "comp"
MATCH_LENGTH = 180

class InvalidOpForState(Exception):
    "Invalid operation for the given state"
    pass

class UserCodeProtocol(protocol.ProcessProtocol):
    def __init__(self, start_fifo, exit_cb, logfile, log_line_cb):
        self.start_fifo = start_fifo
        self.exit_cb = exit_cb
        self.logf = open(logfile,"w")
        self.log_line_cb = log_line_cb

    def childDataReceived(self, childFD, data):
        self.log_line_cb(data)
        self.logf.write(data)
        self.logf.flush()
        os.fsync(self.logf.fileno())

    def processExited(self, status):
        self.exit_cb(status)

    def send_start(self, match_info):
        with open( self.start_fifo, "w" ) as f:
            f.write( json.dumps( match_info ) )

class UserCodeManager(object):
    S_IDLE, S_LOADED, S_STARTED, S_KILLING = range(4)
    state_strings = {
        S_IDLE: "idle",
        S_LOADED: "loaded",
        S_STARTED: "started",
        S_KILLING: "killing"
    }

    def __init__(self, logdir):
        self.logdir = logdir
        self.zone = 0
        self.mode = MODE_DEV
        self.state = UserCodeManager.S_IDLE
        self.state_change_cb = None
        self.log_line_cb = None
        self.logfile = None

        # Current user process protocol and transport
        self.userproto = None
        self.usertransport = None

        # Current directory for user code
        self.userdir = None

        # Deferred for match timer
        self.match_timer = None

    def change_state(self, newstate):
        print "UserCodeManager state: {0} -> {1}".format(UserCodeManager.state_strings[self.state],
                                                         UserCodeManager.state_strings[newstate])
        self.state = newstate
        if self.state_change_cb is not None:
            self.state_change_cb(newstate)

    def load(self, fileobj, type="zip"):
        "Load new code into the robot"

        if self.state != UserCodeManager.S_IDLE:
            "We have code already running"
            raise InvalidOpForState("Cannot load new code whilst existing code is running")

        if self.userproto is not None:
            shutil.rmtree(self.userdir)
            os.remove(self.start_fifo)
            self.userproto = None
            self.userdir = None

        # Directory the user code will be extracted into
        self.userdir = tempfile.mkdtemp(prefix="pyenv-")

        print "Extracting user code to", self.userdir

        # Open the file in transparent (de)compression mode
        if type == "zip":
            with zipfile.ZipFile(fileobj, "r") as zipf:
                zipf.extractall(self.userdir)

        elif type == "tar":
            with tarfile.open(fileobj=fileobj, mode="r") as tarf:
                tarf.extractall(self.userdir)

        self.start_fifo = tempfile.mktemp()
        os.mkfifo(self.start_fifo)

        self.logfile = os.path.join(self.logdir, "log.txt")
        self.userproto = UserCodeProtocol(self.start_fifo,
                                          self.code_exited,
                                          self.logfile,
                                          self._log_line_cb)

        self.usertransport = reactor.spawnProcess(self.userproto,
                                                  sys.executable,
                                                  args = [ sys.executable,
                                                           "-m", "herdsman.loggrok",
                                                           "robot.py",
                                                           "--usbkey", self.logdir,
                                                           "--startfifo", self.start_fifo ],
                                                  env = os.environ,
                                                  path = os.path.join(self.userdir, "user"))
        self.change_state(UserCodeManager.S_LOADED)

    def _log_line_cb(self, *args, **kw):
        if self.log_line_cb is not None:
            self.log_line_cb(*args, **kw)

    def start(self):
        "Send the start info the user code"

        if self.state != self.S_LOADED:
            print "start() called from the wrong state"
            return

        self.userproto.send_start( {"mode": self.mode,
                                    "zone": self.zone} )
        
        if self.mode == MODE_COMP:
            self.match_timer = reactor.callLater(MATCH_LENGTH, self.end_match)

        self.change_state(UserCodeManager.S_STARTED)

    def end_match(self):
        "Called when the match timer expires"
        if self.state == UserCodeManager.S_IDLE:
            "Code has already stopped"
            return

        self.stop()

    def code_exited(self, status):
        "Callback for when the subprocess exits"
        print "Code exited"
        self.change_state(UserCodeManager.S_IDLE)
        self.hw_reset()

    def stop(self):
        if self.state == UserCodeManager.S_IDLE:
            "Code is not running"
            raise InvalidOpForState("stop() called when code isn't running")

        # Send the kill signal
        self.usertransport.signalProcess("KILL")
        self.change_state(UserCodeManager.S_KILLING)

    def hw_reset(self):
        "Reset the robot hardware back to power-on state"
        pass

    def get_state(self):
        return self.state
