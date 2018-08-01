#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: Agent.py
# @time: 2018/7/29 14:35
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
import numpy as np

npr = np.random

class Agent(object):

    __metaclass__ = ABCMeta

    def __init__(self, indv=None, dim=2, fitness_value=-np.inf,
                 fitness_function=None, init_method='random', *args, **kwargs):
        if indv:
            self._indv = indv
            self.dim = len(indv)
        else:
            if init_method == 'rand' or init_method == 'random':
                self._indv = npr.random(dim)
            else:
                self._indv = npr.randn(dim)
            self.dim = dim
        self._fitness_value = fitness_value
        self.fitness_function = fitness_function

    @property
    def indv(self):
        return self._indv

    @indv.setter
    def indv(self, indv):
        self._indv = indv

    @property
    def fitness_value(self):
        return self._fitness_value

    @fitness_value.setter
    def fitness_value(self, fitness_value):
        self._fitness_value = fitness_value

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    def fitness(self, *args, **kwargs):
        self._fitness_value = self.fitness_function(self._indv)
        return self._fitness_value

    def __gt__(self, agent):
        return self._fitness_value > agent.fitness_value

    def __lt__(self, agent):
        return self._fitness_value < agent.fitness_value
