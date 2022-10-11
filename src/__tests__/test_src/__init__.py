
# -*- coding: utf-8 -*-

import os

__path__ = os.path.dirname(__file__)

__all__ = []
for directory in os.listdir(os.getcwd()):
    if directory.startswith('.') or directory.startswith('__') or directory.endswith('.exe'):
        pass
    else:
        __all__.append(directory)

__title__ = 'test_src'
__description__ = 'test cases for the Sofia protocol'
__url__ = 'https://github.com/kesler20/Sofia'
__author__ = 'Kesler Isoko'