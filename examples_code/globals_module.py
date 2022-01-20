# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 12:05:34 2021

@author: manager
"""
# global global_dict


def fun1():
    # global global_dict

    def fun2():
        global global_dict
        global_dict["a1"] = 4

    fun2()
