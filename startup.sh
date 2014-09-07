#!/bin/bash

screen -ls | grep -q "No Sockets found in"
if [ $? -ne 0 ]
then
  echo Some servers still running - kill them before running this script
else 

  echo Starting monitor server
  screen -S monitor -d -m python Monitor/monitor_server.py

  echo Starting socket server
  screen -S socket -d -m python Monitor/monitor.py run_sockets.py

  echo Starting Text-To-Speech server
  screen -S tts -d -m python Monitor/monitor.py run_tts.py

  echo Starting main jarvis server
  screen -S jarvis -d -m python Monitor/monitor.py run_jarvis.py

  sleep 1

  echo Running screens:
  screen -ls

  echo screen -h for help
fi

exit 0
