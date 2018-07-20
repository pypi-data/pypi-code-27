#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 17:55:11 2018

@author: sxwxiaoxiao
"""
import numpy as np
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
