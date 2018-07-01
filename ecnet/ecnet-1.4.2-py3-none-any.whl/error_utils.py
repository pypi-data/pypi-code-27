#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ecnet/error_utils.py
#  v.1.4.2
#  Developed in 2018 by Travis Kessler <Travis_Kessler@student.uml.edu>
#
#  This program contains functions for error calculations
#

import numpy as np
from math import sqrt

# Calculates the root-mean-square error between two arguments of equal length
def calc_rmse(y_hat, y):
	try:
		return(np.sqrt(((y_hat-y)**2).mean()))
	except:
		try:
			return(np.sqrt(((np.asarray(y_hat)-np.asarray(y))**2).mean()))
		except:
			raise ValueError("Error in calculating RMSE. Check input data format.")
			
# Calculates the mean average error between two arguments of equal length 
def calc_mean_abs_error(y_hat, y):
	try:
		return(abs(y_hat-y).mean())
	except:
		try:
			return(abs(np.asarray(y_hat)-np.asarray(y)).mean())
		except:
			raise ValueError("Error in calculating mean average error. Check input data format.")

# Calculates the median absoltute error between two arguments of equal length			
def calc_med_abs_error(y_hat, y):
	try:
		return(np.median(np.absolute(y_hat-y)))
	except:
		try:
			return(np.median(np.absolute(np.asarray(y_hat)-np.asarray(y))))
		except:
			raise ValueError("Error in calculating median absolute error. Check input data format.")

# Calculates the correlation of determination, or r-squared value, between two arguments of equal length
def calc_r2(y_hat, y):
	try:
		y_mean = y.mean()
	except:
		try:
			y_form = []
			for i in range(len(y)):
				y_form.append(y[i][0])
			y_mean = sum(y_form)/len(y_form)
		except:
			raise ValueError("Error in calculating r-squared. Check input data format.")
	try:
		s_res = np.sum((y_hat-y)**2)
		s_tot = np.sum((y-y_mean)**2)
		return(1 - (s_res/s_tot))
	except:
		try:
			s_res = np.sum((np.asarray(y_hat)-np.asarray(y))**2)
			s_tot = np.sum((np.asarray(y)-y_mean)**2)
			return(1 - (s_res/s_tot))
		except:
			raise ValueError("Error in calculating r-squared. Check input data format.")
