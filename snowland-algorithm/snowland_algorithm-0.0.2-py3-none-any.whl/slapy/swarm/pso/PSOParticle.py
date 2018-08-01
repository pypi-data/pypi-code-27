#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: Particle.py
# @time: 2018/7/30 1:53
# @Software: PyCharm

from slapy.swarm.util import Agent
from copy import deepcopy
import numpy as np

npr = np.random


class PSOParticle(Agent):
    def __init__(self, indv=None,
                 dim=2,
                 fitness_value=-np.inf,
                 fitness_function=None,
                 init_method='randn',
                 v0=None,
                 vmax=0.1,
                 pbest=None,
                 w=0.8,
                 c1=2,
                 c2=2,
                 *args, **kwargs):
        """
        :param indv: 粒子位置
        :param dim: 粒子维度
        :param fitness_value: 粒子适应度
        :param v0: 粒子初速度
        :param vmax: 最大速度
        :param pbest: 当前粒子的历史最优
        :param w: 权重因子
        :param c1: 历史最优加速因子
        :param c2: 全局最优加速因子
        :param args:
        :param kwargs:
        """
        super().__init__(indv=indv, dim=dim,
                         fitness_value=fitness_value,
                         init_method=init_method,
                         fitness_function=fitness_function,
                         *args, **kwargs)
        self.w = w
        self.c1, self.c2 = c1, c2
        self.vmax = vmax
        self.v = v0 if v0 else npr.rand(self.dim)
        self.pbest = pbest if pbest else deepcopy(self)
        self.fitness()

    @property
    def indv(self):
        return super(PSOParticle, self).indv

    def update(self, gbest, *args, **kwargs):
        r1, r2 = npr.rand(2)
        self._indv += self.v
        self.v = self.w * self.v + self.c1 * r1 * (self.pbest.indv - self.indv) + self.c2 * r2 * (
                    gbest.indv - self.indv)
        ind = np.abs(self.vmax) > np.abs(self.v)
        self.v[ind] = self.vmax * np.sign(self.v[ind])
        self.fitness()
        if self.fitness_value > self.pbest.fitness_value:
            self.pbest = deepcopy(self)

    def fitness(self, *args, **kwargs):
        return super(PSOParticle, self).fitness(self.indv, *args, **kwargs)
