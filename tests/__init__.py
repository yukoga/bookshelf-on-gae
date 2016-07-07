# -*- coding: UTF-8 -*-

import os
import sys

current = os.path.abspath(os.path.dirname(__file__))
path_dir = sys.path

if current not in path_dir:
    sys.path.insert(0, current)
