#!/bin/usr/env python3

#### CS28510 SAMANTHA STAGG PROJECT 2 ####

import math
import numpy as np
import matplotlib.pyplot as plt

MIN_LEVEL = 4
MAX_LEVEL = 30

def simpsons_rule(f, a, b):
	return ((b-a)/6)*(f(a) + 4*f((a+b)/2) + f(b))

def plot1(fn_name, nums_evals, tolerances):
	log_ns = []
	log_ts = []
	for n in nums_evals:
		log_ns.append(np.log(n))
	for t in tolerances:
		log_ts.append(np.log(1/t))
	fig = plt.figure()
	tols, = plt.plot(log_ns, log_ts)
	plt.title(fn_name)
	plt.xlabel('log(number of evaluations)')
	plt.ylabel('log(1/tolerance)')
	if ' ' in fn_name:
		fn_name = fn_name.replace(' ', '_').replace('<', \
				  '_less_than_').replace('/', '_over_')
	fig.savefig(fn_name+'_num_evals_vs_tolerances.pdf')

def plot2(fn_name, actual_errors, tolerances):
	log_es = []
	log_ts = []
	for e in actual_errors:
		if e != 0:
			log_es.append(np.log(1/e))
	for t in tolerances:
		if actual_errors[tolerances.index(t)] != 0:
			log_ts.append(np.log(1/t))
	fig = plt.figure()
	tols, = plt.plot(log_es, log_ts)
	plt.title(fn_name)
	plt.xlabel('log(1/actual error)')
	plt.ylabel('log(1/tolerance)')
	if ' ' in fn_name:
		fn_name = fn_name.replace(' ', '_').replace('<', \
				  '_less_than_').replace('/', '_over_')
	fig.savefig(fn_name+'_errors_vs_tolerances.pdf')

def plot3(fn_name, interval_lengths, interval):
	int_lens = []
	for i in interval_lengths:
		int_lens.append(-np.log(i))
	xs = np.linspace(interval[0], interval[1], len(interval_lengths))
	fig = plt.figure()
	lengths, = plt.plot(xs, int_lens)
	plt.title(fn_name)
	plt.xlabel('x value')
	plt.ylabel('-log(good interval length)')
	if ' ' in fn_name:
		fn_name = fn_name.replace(' ', '_').replace('<', \
				  '_less_than_').replace('/', '_over_')
	plt.savefig(fn_name+'_good_interval_lens.pdf')

def integrate(f, a, b, tolerance, level, num_evals, good_ints):
	num_evals += 1
	coarse_approx = simpsons_rule(f, a, b)
	midpt = (a+b)/2
	fine_approx = simpsons_rule(f, a, midpt) + simpsons_rule(f, midpt, b)
	if level == MAX_LEVEL or abs(coarse_approx - fine_approx) <= tolerance*15:
		level -= 1
		good_ints.append(b - a)
		return (num_evals, fine_approx, good_ints)
	else:
		return integrate(f, a, midpt, tolerance/2, level+1, num_evals, \
			   good_ints) + integrate(f, midpt, b, tolerance/2, \
			   level+1, num_evals, good_ints)

if __name__ == '__main__':
	fns = {'x^4': lambda x: x**4, 'sqrt(sin(pi*x))': lambda x: \
		   math.sqrt(np.sin(np.pi*x)), 'x^6': lambda x: x**6, \
		   '1 if x<(1/sqrt(2)) else 0': lambda x: 1 \
		   if x<(1/math.sqrt(2)) else 0}
	ints = [(0, 1), (0, 1/2), (-1, 1), (0, 1)]
	tolerances = [1*(10**(-2)), 1*(10**(-4)), 1*(10**(-6))]
	i = 0
	for fn in fns:
		nums_evals = []
		actual_errors = []
		for t in tolerances:
			integral = integrate(fns[fn], ints[i][0], ints[i][1], t, 0, 0, [])
			(num_evals, fine_approx, good_ints) = (integral[0], integral[1], 
											       integral[2])
			actual = integrate(fns[fn], ints[i][0], ints[i][1], 1*(10**(-9)), \
							   0, 0, [])[1]
			actual_errors.append(abs(actual-fine_approx))
			nums_evals.append(num_evals)
			if t == 10**-4:
				plot3(fn, good_ints, ints[i])
		plot1(fn, nums_evals, tolerances)
		plot2(fn, actual_errors, tolerances)
		i += 1





