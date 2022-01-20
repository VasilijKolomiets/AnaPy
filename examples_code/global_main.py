# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 12:04:50 2021

@author: manager
"""
from globals_module import *
global global_dict

global_dict = dict.fromkeys(["a1", "a2", "a3", "a4"])


def fun0():
    # global global_dict
    fun1()


fun0()
