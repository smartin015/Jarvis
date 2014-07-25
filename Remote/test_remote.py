from remote_client import send_remote_cmd

send_remote_cmd("TheMothership", "audio", "Remote/setaudio.py speaker")

raw_input("Enter to quit")

send_remote_cmd("TheMothership", "audio", "QUIT")
