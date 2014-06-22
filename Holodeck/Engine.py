from string import capitalize
import threading
from Holodeck.Settings import Pipe as P
import time
import logging
from pygame.time import Clock
import types
from string import capitalize
import bisect

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
    meta = dict(self.META) #Make a copy
    if not meta.get('id'):
      meta['id'] = classname_to_id(self.__name__)
    if not meta.get('img'):
      meta['img'] = meta['id']+".png"
    if not meta.get('text'):
      meta['text'] = capitalize(meta['id'])
    if not meta.get('tab'):
      meta['tab'] = self.__module__.split(".")[-1].lower()
  
    return meta


  def get_blacklist(self):
    """ Return a list of typenames that this effect 
        should not run alongside
    """
    return []

  def handle_blacklist(self):
    blacklist_names = [cls.__name__ for cls in self.get_blacklist()]

    for ename in blacklist_names:
      effect = self.active_effects.get(ename)
      if effect:
        effect.request_exit()
    self.logger.debug("Blacklist handled")  

  def insert_into_pipeline(self):
    for (pipe_id, con) in self._get_mapping().items():
      if self.pipes.get(pipe_id) is None:
        continue
    
      i = bisect.bisect_right([c[1] for c in self.pipes[pipe_id]], con[1])
      self.pipes[pipe_id].insert(i,con)

  def register(self):
    """ Effect injects itself into its own location(s) 
        in the controller pipeline
    """
    # TODO: blacklist booting
    
    # Add to pipeline
    self.insert_into_pipeline()

    self.active_effects[self.__class__.__name__] = self

  def _get_mapping(self):
    # Useful for transitions on top of effects
    return self.get_mapping()

  def get_mapping(self):
    raise Exception("Unimplemented")

  def remove_from_pipeline(self):
    """ Removes ourselves from the pipeline """
    # TODO: Mutex this!
    for (pipe_id, con) in self._get_mapping().items():
      if not self.pipes.get(pipe_id):
        continue
      try:
        idx = self.pipes[pipe_id].index(con)
        del self.pipes[pipe_id][idx]
      except ValueError:
        print self.pipes
        raise

  def remove(self):
    self.remove_from_pipeline()

    # Remove from active effects
    del self.active_effects[self.__class__.__name__]

    # Notify the holodeck that we're dead
    self.remove_cb(self)

  def request_exit(self):
    """ Tell this effect to start the process of dying.
        For most effects, it just removes it immediately.
    """
    self.logger.debug("Exiting")
    self.remove()

class HolodeckEngine():
  
  def __init__(self, effect_list, pipelines, update_funcs, state_callback=None):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
        
    self.update_funcs = update_funcs

    # Create a dictionary of effects keyed by class name
    self.effectClasses = effect_list

    self.state_callback = state_callback

    # When effects are instantiated, they are listed here.
    # New effects can request existing effects to go away,
    # Which allows for fading in/out.
    self.activeEffects = dict()

    # Each array represents a pipeline of control functions, linked
    # from effect objects.
    # Subsequent functions are passed in the previous functions' outputs.
    # Composition is left-to-right
    self.pipelines = {}
    self.initial_pipe_values = {}
    for pipe in pipelines:
      self.pipelines[pipe] = []
      self.initial_pipe_values[pipe] = pipelines[pipe]

  def compose(self, pipe_names):
    # Composes each controller pipeline into a single environment
    env = []
    for name in pipe_names:
      composite = self.initial_pipe_values[name]
      for (con, priority) in self.pipelines[name]:
        composite = con(composite)
      env.append(composite)

    return env

  def start_pipeline(self):
    c = Clock()
    self.logger.debug("Beginning main loop")

    # Create a thread for each pipeline controller
    for (deps, func) in self.update_funcs:
      t = threading.Thread(target = self.update, args=(deps, func, 30))
      t.daemon = True
      t.start()
    
  def update(self, deps, callback, max_fps):
    c = Clock()
    while True:
      env = self.compose(deps)
      callback(*env)
      c.tick(max_fps)

  def handle_effect_exit(self, effect):
    state = {classname_to_id(effect.__class__.__name__): False}
    self.state_callback(state)

  def get_meta(self):
    meta = {}
    for e in self.effectClasses:
      e_meta = self.effectClasses[e].get_meta()
      e_meta['active'] = (e in self.activeEffects)

      if not meta.get(e_meta['tab']):
        meta[e_meta['tab']] = {}

      meta[e_meta['tab']][e_meta['id']] = e_meta
    return meta

  def handle(self, request):
    # Request is in JSON format,
    # Specifying any of the following keys with a boolean true/false to update:
    #    - cave, town, river, ocean (environment effects)
    #    - rain, snow, campfire (modifiers)
    #    - day, night (times. transitions w/ sunrise & sunset)
    #    - battle (big, flashy, for beginning of fights)
    #
    # See self.effectClasses for a full list
    self.logger.debug("Got request %s" % str(request))
    try:

      for (req, turn_on) in request.items():
        req = id_to_classname(req)
        if turn_on:
          self.logger.info("Adding " + req)
          
          if req in self.activeEffects:
            self.logger.error("Effect already in effect")
            continue
          
          # Create a new effect with this request.
          # This may affect other active effects
          eff = self.effectClasses[req](self.pipelines, self.activeEffects, self.handle_effect_exit)

          self.logger.info("Registering")
          eff.register()

          # Tell the server this was activated
          self.state_callback({classname_to_id(req): True})

        elif self.activeEffects.get(req):
          self.logger.info("Removing " + req)
          self.activeEffects[req].request_exit()
    except:
       import traceback
       traceback.print_exc()
       raise


