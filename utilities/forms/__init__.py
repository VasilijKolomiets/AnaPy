# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 12:37:22 2022

@author: manager
"""
# import os
import sys
from pathlib import Path

here_path = Path(__file__)
up_folder = here_path.parent.parent.resolve()
sys.path.append(up_folder)
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
