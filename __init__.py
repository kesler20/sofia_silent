
# -*- coding: utf-8 -*-

import os

version_info = (0, 0, 1)
__version__ = ".".join([str(v) for v in version_info])

__path__ = os.path.dirname(__file__)
__all__ = []
for directory in os.listdir(os.getcwd()):
    if directory.startswith('.') or directory.startswith('__') or directory.endswith('.exe'):
        pass
    else:
        __all__.append(directory)

__title__ = 'Sofia'
__description__ = 'Source code of the Software inteligenza artificiale Sofia Virtual Assistant'
__url__ = 'https://github.com/kesler20/Sofia'

__author__ = 'Kesler Isoko'
