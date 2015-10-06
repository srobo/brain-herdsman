# Hacky routines that do not belong here for interacting with the
# power board
import pyudev
from sr.robot.power import Power

def get_power():
    "Return a power board"

    def _udev_compare_serial(x, y):
        """Compare two udev serial numbers"""
        return cmp(x["ID_SERIAL_SHORT"],
                   y["ID_SERIAL_SHORT"])

    udev = pyudev.Context()
    devs = list(udev.list_devices( ID_MODEL = "Power_board_v4" ))
    # Sort by serial number
    devs.sort( cmp = _udev_compare_serial )

    if not len(devs):
        return None

    dev = devs[0]
    return Power("",
                 int(dev["BUSNUM"]),
                 int(dev["DEVNUM"]),
                 dev["ID_SERIAL_SHORT"])
    


