import os
import glob
import inspect
import sys
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

from Locations import *
from Effects import *
from Atmosphere import *

def get_all_effects():
  
  # TODO: To get rid of the import * stuff, try iterating through 
  # modules and building a class list
  """
  for modname in __all__:
    if modname == "__init__":
      pass

    mod = __import__("Holodeck.Effects." + modname)
    print inspect.getmembers(mod)
  """
  
  effect_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)
  return dict([(k,v) for k,v in effect_list if k.endswith('Effect')])
