import types

class EffectTemplate():
  META = {
    'tab': None,
    'id': None,
    'text': None,
    'img': None,
  }

  def __init__(self, active_effects, pipes):
    self.should_exit = False
    self.pipes = pipes
    self.active_effects = active_effects
    self.setup()

  def setup(self):
    pass

  def get_blacklist(self):
    """ Return a list of typenames that this effect 
        should not run alongside
    """
    return []

  def register(self):
    """ Effect injects itself into its own location(s) 
        in the controller pipeline
    """
    # TODO: blacklist booting

    # Add to pipeline
    for (pipe_id, con) in self.get_mapping().items():
      self.pipes[pipe_id].append(con)
      self.pipes[pipe_id].sort(key=lambda con:con[1])

    # Add to active effects
    self.active_effects[self.__class__.__name__] = self


  def get_mapping(self):
    raise Exception("Unimplemented")

  def remove(self):
    """ Removes ourselves from the pipeline """
    # TODO: Mutex this!
    for (pipe_id, con) in self.get_mapping().items():
      try:
        idx = self.pipes[pipe_id].index(con)
        del self.pipes[pipe_id][idx]
      except ValueError:
        print self.pipes
        raise

    # Remove from active effects
    del self.active_effects[self.__class__.__name__]

    # TODO: Notify the holodeck that we're dead

  def request_exit(self):
    """ Tell this effect to start the process of dying 
    """
    self.should_exit = True

  def post_render(self):
    """ Called once per frame for update purposes. 
        Remember to check self.should_exit() here
    """
    if self.should_exit:
      self.remove()



