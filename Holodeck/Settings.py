
SERVER_LIST = ["Jarvis", "TheMothership"]
SERVER_PORT = 9601

MASTER_SERVER = "Jarvis"

class Pipe():
  RING = "towerRing"
  TOWER = "tower"
  LIGHTS = "lights"
  WINDOWIMG = "windowimg"
  WALLIMG = "wallimg"
  FLOOR = "floor"
  WINDOWTOP = "windowtop"
  WINDOWBOT = "windowbot"
  TEMP = "temp"
  SOUND = "sound"

  @classmethod
  def items(self):
    return [v for (k,v) in self.__dict__.items() 
            if type(v) is str 
            and not v.startswith("__")
            and not k.startswith("__")]
