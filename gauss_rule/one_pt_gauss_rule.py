#!/usr/bin/env python3

#### CS28510 SAMANTHA STAGG PROJECT 3 ####

import numpy as np
from scipy.integrate import quad
import math
from sympy import *
from scipy.optimize import fsolve

a = 0
b = 1

def GR_1(f, p, c, d):
	p_g = fsolve(lambda q: d**(p+1)*(d/(p+2) - q/(p+1)) - (c**(p+1)*(c/(p+2) - \
				 q/(p+1))), 1)
	x_val = fsolve(lambda x: f(x) - 1, 1)
	w_g = quad(lambda x: f(x_val[0]), c, d)[0]
	return w_g*f(p_g[0])

def compute(f, p, n):
	pts = list(np.linspace(a, b, n + 1))
	ints = []
	for pt in pts[:len(pts) - 1]:
		ints.append([pt])
	i = 0
	for pt in pts[1:]:
		ints[i].append(pt)
		i += 1
	integral = 0
	for interval in ints:
		integral += GR_1(lambda x: f(x)*(x**p), p, interval[0], interval[1])
	return integral

if __name__=='__main__':
	fns = {'x': lambda x: x, 'sqrt(x)': lambda x: x**(1/2), 
		   '(1-sin(x))^2': lambda x: (1 - np.sin(x))**2, 'sqrt(x)/sqrt(sin(x/2)':
		    lambda x: (x**(1/2))/((np.sin(x/2))**(1/2))}
	ps = [2, -0.5, -0.5, -0.5]
	ns = [[5], [4, 40], [5, 50, 100], [2, 10]]
	i = 0
	for fn in fns:
		integral_vals = []
		for n in ns[i]:
			integral = compute(fns[fn], ps[i], n)
			integral_vals.append((n, integral))
		if i == 0:
			f = open('integral_values.txt', 'w+')
		else:
			f = open('integral_values.txt', 'a+')
		for val in integral_vals:
			if integral_vals.index(val) != len(integral_vals) - 1:
				f.write('f(x) = ' + fn + ' integral value for p = ' + \
						str(ps[i]) + ', n = ' + str(val[0]) + ' is ' + \
						str(val[1]) + '.\n')
			else:
				f.write('f(x) = ' + fn + ' integral value for p = ' + \
						str(ps[i]) + ', n = ' + str(val[0]) + ' is ' + \
						str(val[1]) + '.\n\n---------------\n\n')
		f.close()
		i += 1






