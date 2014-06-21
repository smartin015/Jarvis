#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))


# This creates the holodeck once, making it global for all
# future connections.
from Holodeck.holodeck_controller import JarvisHolodeck
jarvisdecksrv = JarvisHolodeck() 
dt = threading.Thread(target=jarvisdecksrv.serve_forever)
dt.daemon = True
dt.start()

from mod_pywebsocket.standalone import _main as run_standalone
run_standalone(["-d", "Holodeck/web", "-p", "8880"])
