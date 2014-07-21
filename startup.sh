#!/bin/bash
screen -S mon -d -m python Monitor/monitor_server.py
screen -S tts -d -m python Monitor/monitor.py run_tts.py
screen -S jarvis -d -m python Monitor/monitor.py run_jarvis.py
screen -S sock -d -m python Monitor/monitor.py run_sockets.py
