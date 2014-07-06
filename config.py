import socket

_hostname = socket.gethostname()

# TODO: Store ALL these settings in a database

ROOMS = ["livingroom", "hackspace"]

SOUND_PATH = "Assets/Sounds/"

OUTPUTS = {
  "livingroom": {
    "RF": ("RFController", "A9MDTZJF", 115200),
    "tracklight": ("RelayController", "A602QORA", 9600),
    "windowlight": ("RGBSingleController", "A9MX5JNZ", 9600),
    "couchlight": ("RGBSingleController", "A70257T7", 9600),
    "tower": ("RGBMultiController", "A9OZNP19", 115200),
  }
}

TTS = {
  "desk_tts": {
    "device": "pci-0000:00:1d.7-usb-0:4.7.4:1.0",
    "host": _hostname,
    "port": 9000,
  },
  "livingroom_tts": {
    "device": "pci-0000:00:1d.7-usb-0:4.6:1.0",
    "host": _hostname,
    "port": 9001,
  },
  "hackspace_tts": {
    "device": "pci-0000:00:1d.7-usb-0:4.5:1.0",
    "host": _hostname,
    "port": 9002,
  },
}

INPUTS = {
  "livingroom": {
    "tts": ["desk_tts", "livingroom_tts"],
  },
  "hackspace": {
    "tts": ["hackspace_tts"]
  }
}
