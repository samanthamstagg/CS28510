#!/usr/bin/env python3

#### SAMANTHA STAGG CMSC 28510 PROFESSOR DUPONT ####

import sys
import matplotlib.pyplot as plt
import numpy as np

dx = (np.pi/2)/100

def interp():
	x = []
	y = []
	for i in range(0, 101):
		x.append(i)
		y.append(np.sin(i*dx))
	return (x, y)

def interpolater(lower, upper):
	xs = np.linspace(lower, upper, (upper-lower)*100)
	yinterp = np.interp(xs, x, y)
	errors = []
	t_errors = []
	for i in xs:
		yinter =  yinterp[np.where(xs==i)[0][0]]
		sine = np.sin(i*dx)
		errors.append(sine - yinter)
		t_errors.append(np.sin(i*dx)*(dx*dx)/8)
	fig = plt.figure()
	errs, = plt.plot(xs, errors, label='Errors')
	t_errs, = plt.plot(xs, t_errors, label='Theoretical Errors',
					   linestyle='--', color='pink')
	plt.title(r'Error in Interpolating $sin(x)$ on $[x_{' + 
				str(lower) + '}$, $x_{' + str(upper) + '}]$')
	plt.legend()
	fig.savefig('x'+str(lower)+'_x'+str(upper)+'.pdf')
	return

if __name__ == "__main__":
	lower_bound = sys.argv[1]
	upper_bound = sys.argv[2]
	if int(lower_bound) in range(0, 101) and int(upper_bound) in range(0, 101):
		try:
			interpolater(int(lower_bound), int(upper_bound))
		except ValueError:
			raise ValueError('Upper and lower bounds must be whole numbers')
	else:
		raise ValueError('Range must be in [0, 100]')
