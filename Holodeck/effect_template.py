import types
import logging
from string import capitalize

def id_to_classname(cmd):
  return "%sEffect" % (capitalize(cmd))

def classname_to_id(key):
  return key[:-6].lower()

class EffectTemplate():
  META = {
    'tab': None,
    'id': None,
    'text': None,
    'img': None,
  }

  def __init__(self, pipes, active_effects, remove_cb):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.remove_cb = remove_cb
    self.should_exit = False
    self.pipes = pipes
    self.active_effects = active_effects
    self.logger.debug("Entering setup")
    self.setup()
    self.logger.debug("Setup complete")

  def setup(self):
    pass

  @classmethod
  def get_meta(self):
    meta = self.META
    if not meta.get('id'):
      meta['id'] = classname_to_id(self.__name__)
    if not meta.get('img'):
      meta['img'] = meta['id']+".png"
    if not meta.get('text'):
      meta['text'] = capitalize(meta['id'])
    return meta


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
      if self.pipes.get(pipe_id) is None:
        continue

      self.pipes[pipe_id].append(con)
      self.pipes[pipe_id].sort(key=lambda con:con[1])

    self.active_effects[self.__class__.__name__] = self

  def get_mapping(self):
    raise Exception("Unimplemented")

  def remove(self):
    """ Removes ourselves from the pipeline """
    # TODO: Mutex this!
    for (pipe_id, con) in self.get_mapping().items():
      if not self.pipes.get(pipe_id):
        continue

      try:
        idx = self.pipes[pipe_id].index(con)
        del self.pipes[pipe_id][idx]
      except ValueError:
        print self.pipes
        raise

    # Remove from active effects
    del self.active_effects[self.__class__.__name__]

    # Notify the holodeck that we're dead
    self.remove_cb(self)

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



