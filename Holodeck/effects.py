from Holodeck.holodeck import Pipe as P

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

class RainEffect(Effect):

  def inject_into(self, pipes):
    pass


class BattleEffect(Effect):

  def inject_into(self, pipes):
    pass


class DayEffect(Effect):

  def inject_into(self, pipes):
    pipes[P.LIGHTS].insert((self.lights, 1))

  def lights(self, prev):
    return True


