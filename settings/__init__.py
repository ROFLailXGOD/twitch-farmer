# -*- coding: utf-8 -*-

try:
    from .local import *
except ImportError:
    import sys
    print('No settings/local.py file!!! Copy it from settings/local.py.skeleton file!')
    sys.exit(1)
