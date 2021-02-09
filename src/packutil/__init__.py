from . import versions

try:
    from . import version
except ImportError:
    # not possible to import its own version while building the first time
    pass
