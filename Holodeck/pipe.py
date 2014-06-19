
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
    return [a for a in self.__dict__.values() if type(a) is str and not a.startswith("__")]
