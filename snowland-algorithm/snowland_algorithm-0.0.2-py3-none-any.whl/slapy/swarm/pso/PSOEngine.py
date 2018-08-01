#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: PSOEngine.py
# @time: 2018/7/30 1:54
# @Software: PyCharm

from slapy.swarm.util import Engine
from slapy.swarm.util import Agent
from matplotlib import pylab as plt
from copy import deepcopy
from abc import ABCMeta, abstractmethod
import numpy as np
from slapy.swarm.pso.PSOParticle import PSOParticle

npa = np.array


class PSOEngine(Engine):
    __metaclass__ = ABCMeta

    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, fitness_function=None,
                 w=0.8, c1=2, c2=2, min_fitness_value=-np.inf, agents=None,
                 gbest: Agent = None, *args, **kwargs):
        super().__init__(population_size=population_size,
                         steps=steps,
                         eps=eps,
                         dim=dim,
                         min_fitness_value=min_fitness_value,
                         agents=agents,
                         fitness_function=fitness_function
                         )
        self.w = w
        self.c1, self.c2 = c1, c2
        self.gbest = gbest if gbest else None
        self.mean = []
        self.max = []
        self.best = []

    def fitness(self, *args, **kwargs):
        return super(PSOEngine, self).fitness()

    def initialize(self, *args, **kwargs):
        if self.agents is None:
            self.agents = [PSOParticle(**(self.__dict__)) for _ in range(self.population_size)]

        self.gbest = self.agents[0]
        for each in self.agents:
            if each > self.gbest:
                self.gbest = deepcopy(each)

    def update(self, *args, **kwargs):
        [each.update(self.gbest, *args, **kwargs) for each in self.agents]
        for each in self.agents:
            if each > self.gbest:
                self.gbest = deepcopy(each)

    def analysis(self, *args, **kwargs):
        print('-' * 15)
        print(self.gbest.__dict__)
        print(self.best)
        print(self.mean)
        print(self.max)
        print('-' * 15)
        plt.title('itor in each steps')
        gca1 = plt.plot(self.mean, 'b-')
        gca2 = plt.plot(self.max, 'g-')
        gca3 = plt.plot(self.best, 'r-')
        # plt.legend([gca1, gca2, gca3], ['mean', 'max', 'best'])
        plt.show()

    def record(self, *args, **kwargs):
        fitness_list = npa([each.fitness_value for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(self.gbest.fitness_value)


if __name__ == '__main__':
    def fun(x):
        x, y = x
        if 0 < x < 1 and 0 < y < 1:
            return x + 2 * y - x * y + np.sin(x * y)
        else:
            return -1


    engine = PSOEngine(vmax=0.01, min_fitness_value=-1, dim=2, fitness_function=fun, steps=100)
    engine.run()
