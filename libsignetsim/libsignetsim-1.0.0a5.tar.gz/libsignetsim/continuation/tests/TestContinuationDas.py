#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014-2017 Vincent Noel (vincent.noel@butantan.gov.br)
#
# This file is part of libSigNetSim.
#
# libSigNetSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libSigNetSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libSigNetSim.  If not, see <http://www.gnu.org/licenses/>.

"""

	Testing the computation of equilibrium curves

"""

from libsignetsim import SbmlDocument, EquilibriumPointCurve
from unittest import TestCase
from os.path import join, dirname
from os import getcwd

class TestContinuationDas(TestCase):
	""" Tests high level functions """

	def testAllReductions(self):

		vars = ['ras_gtp', 'ras_gdp', 'sos', 'sos_ras_gtp', 'sos_ras_gdp']
		tests = [
			(0, 1), (0, 2), (0, 3), (0, 4),
			(1, 2), (1, 3), (1, 4),
			(2, 3), (2, 4),
			(3, 4)
		]

		results = []

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")

		for test in tests:

			doc = SbmlDocument()
			doc.readSbmlFromFile(join(testfiles_path, "ras_das_full.xml"))
			doc.model.build(reduce=False)
			doc.model.listOfConservationLaws.build()

			vars_to_reduce = set(list(test))
			ind_to_keep = set(range(5)).difference(vars_to_reduce)
			vars_to_keep = [vars[ind] for ind in ind_to_keep]

			t_ep_curve = EquilibriumPointCurve(doc.model)
			t_ep_curve.setParameter(doc.model.listOfVariables.getBySbmlId("total_1"))
			t_ep_curve.setRange(0, 10000)
			t_ep_curve.setDs(1)
			t_ep_curve.setMaxSteps(5000)
			t_ep_curve.build(vars_to_keep=vars_to_keep)
			t_ep_curve.run()

			if t_ep_curve.getCurves() != None:
				x, ys = t_ep_curve.getCurves()
				results.append(len(x))

				if len(x) > 1:
					if x[len(x)-1] > 0:
						print("Model with %s : Success" % str(vars_to_keep))
					else:
						print("Model with %s : Went backward" % str(vars_to_keep))
				else:
					print("Model with %s : Failed" % str(vars_to_keep))
			else:
				print("Model with %s : Failed" % str(vars_to_keep))