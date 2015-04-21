from collections import namedtuple
import json
import os
import pyudev
from usercode import MODE_DEV, MODE_COMP
from subprocess import check_call, CalledProcessError

CompSettings = namedtuple("CompSettings", ["mode", "zone", "arena"])

def load_from_usbkey():
    "Try to load settings from a USB key"
    compkey_dir = "/tmp/comp-key"
    comp_info_path = os.path.join(compkey_dir, "mode.json")

    if not os.path.exists(compkey_dir):
        os.mkdir(compkey_dir)

    # Iterate through disks to see if there's one that's a competition-mode
    # USB key
    c = pyudev.Context()

    for dev in c.list_devices( subsystem = "block", DEVTYPE="partition" ):
        if dev.find_parent( subsystem="usb" ) is None:
            "We're looking for a USB key, and this isn't one"
            continue

        # Try mounting it
        try:
            with open("/dev/null", "w") as null_f:
                check_call( [ "mount", "-o", "ro", dev.device_node, compkey_dir ],
                            stderr = null_f, stdout = null_f )
        except CalledProcessError:
            # Not a device we can mount
            continue

        if not os.path.exists(comp_info_path):
            check_call( [ "umount", compkey_dir ] )
            continue

        with open(comp_info_path, "r") as f:
            comp_info = json.load(f)

        check_call( [ "umount", compkey_dir ] )
        return CompSettings( mode = MODE_COMP,
                             zone = comp_info["zone"],
                             arena = comp_info["arena"] )

    return None

def load_mode_settings():
    "Return competition mode settings"
    
    usb_settings = load_from_usbkey()
    if usb_settings is not None:
        return usb_settings

    return CompSettings( mode = MODE_DEV,
                         zone = 0,
                         arena = "A" )
