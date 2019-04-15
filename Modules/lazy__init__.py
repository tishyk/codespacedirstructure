import types, sys, importlib

# https://youtu.be/0oTh1CXRaQ0?t=7480

# ---spam-
#      |
#       --- module1
#               |
#               Class1, Class2 ....

# List the exported symbols by module
_submodule_exports = {'.module1': ['ClassName']}  # __all__ variable from imported module

# Make a {name:modname} mapping
_submodule_by_name = {
    name: modulename
    for modulename in _submodule_exports
    for name in _submodule_exports[modulename]
}


class OnDemandModule(types.ModuleType):
    def __getattr__(self, item):
        module_name = _submodule_by_name.get(item)
        if module_name:
            module = importlib.import_module(module_name, __package__)
            print('Loaded', item)
            value = getattr(module, item)
            setattr(self, item, value)
            return value
        raise AttributeError('No attribute {}'.format(item))


newmodule = OnDemandModule(__name__)
newmodule.__dict__.update(globals())
newmodule.__all__ == list(_submodule_by_name)
sys.modules[__name__] = newmodule
