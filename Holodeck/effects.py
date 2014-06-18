from Holodeck.holodeck import Pipe as P
from Outputs.RGBMultiController import NLIGHTS, NRING

class Effect():
  META = {
    'category': None,
    'image': None,
    'name': None,
    'description': None,
  }

  def get_blacklist(self):
    """ Return a list of typenames that this effect 
        should not run alongside
    """
    return []

  def inject_into(self, pipes):
    """ Effect injects itself into its own location(s) 
        in the controller pipeline
    """

    raise Exception("Unimplemented")

  def request_exit(self):
    """ Tell this effect to start the process of dying 
    """

  def post_render(self, holodeck):
    """ Called once per frame for update purposes. """
    pass


class ForestEffect(Effect):
  
  def __init__(self):
    self.counter = 0

  def inject_into(self, pipes):
    pipes[P.FLOOR].insert((self.floor, 1))
    pipes[P.WINDOWTOP].insert((self.window_top, 1))
    pipes[P.WINDOWBOT].insert((self.window_bot, 1))

  def floor(self, prev):
    return [55, 155, 55]

  def window_top(self, prev):
    return [158, 158, 255]

  def window_bot(self, prev):
    return [100, 50, 20]

  def post_render(self, holodeck):
    self.counter += 1

class RainEffect(Effect):

  def inject_into(self, pipes):
    pipes[P.TOWER].insert((self.tower, 1))
    pipes[P.RING].insert((self.ring, 1))

  def tower(self, prev):
    return [[0, 0, 255]]*105

  def ring(self, prev):
    return [[128, 128, 255]]*24


class BattleEffect(Effect):

  def inject_into(self, pipes):
    pass


class DayEffect(Effect):

  def inject_into(self, pipes):
    pipes[P.LIGHTS].insert((self.lights, 1))

  def lights(self, prev):
    return True


