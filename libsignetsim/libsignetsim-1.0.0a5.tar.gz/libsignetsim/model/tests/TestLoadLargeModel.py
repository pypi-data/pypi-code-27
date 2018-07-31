#!/usr/bin/env python
""" TestLoadLargeModel.py


	Testing the research for conservation laws, and the subsequent reduction


	Copyright (C) 2016 Vincent Noel (vincent.noel@butantan.gov.br)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

from libsignetsim.model.SbmlDocument import SbmlDocument
from libsignetsim.simulation.TimeseriesSimulation import TimeseriesSimulation
from libsignetsim.settings.Settings import Settings

from unittest import TestCase
from os.path import join, dirname, isdir
from os import mkdir, getcwd

class TestLoadLargeModel(TestCase):
	""" Tests high level functions """


	def testLoadGerared(self):

		Settings.verboseTiming = 3

		testfiles_path = join(join(getcwd(), dirname(__file__)), "files")
		sbml_doc = SbmlDocument()
		sbml_doc.readSbmlFromFile(join(testfiles_path, "gerard.xml"))

		# sbml_model = sbml_doc.getModelInstance()
		# sbml_model.build()

		model = sbml_doc.getModelInstance()

		sim = TimeseriesSimulation([model], time_min=0, time_ech=1, time_max=100)
		sim.run()
		t, y = sim.getRawData()[0]

		Settings.verboseTiming = 0