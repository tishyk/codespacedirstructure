# Controls behavior of 'from module import *'
__all__ = ['Foo']  # from .foo import * will import Foo class only

# for __init__.py __all__  variable ---> __all__ = (foo.__all__ + bar.__all__)

class Foo: ...

class Bar: ...

class Defined: ...


# export decorator should be defined in __init__.py
def export(defn):
  globals()[defn.__name__] = defn
  __all__.append(defn.__name__)
  return defn
 
 
 from . import export
 
 
 @export
 class ClassonExport: pass
 
 
 @export
 def funconexport():pass
  
