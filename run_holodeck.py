#!/usr/bin/env python

from mod_pywebsocket.standalone import _main as run_standalone
run_standalone(["-d", "Holodeck/web", "-p", "8880"])
