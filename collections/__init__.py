# Should be reimplemented for MicroPython
# Reason:
# CPython implementation brings in metaclasses and other bloat.
# This is going to be just import-all for other modules in a namespace package
from ucollections import *
try:
    from .defaultdict import defaultdict
except Exception as e:
    print(e)
    pass
try:
    from .deque import deque
except ImportError:
    pass

class Mapping:
    pass

class MutableMapping:
    pass
