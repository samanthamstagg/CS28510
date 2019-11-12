#!/bin/usr/env python3

import numpy as np
from scipy.sparse import diags
import time

### CS 28510 SAMANTHA STAGG PROJECT 6 ###

class Edge_Tridiag:

	def __init__(self, n, d_form, a_form, b_form, e_form):
		self.d = np.zeros(n)
		self.a = np.zeros(n-1)
		self.b = np.zeros(n-1)
		self.e = np.zeros(n-2)
		self.dim = n
		self.d_form = d_form
		self.a_form = a_form
		self.b_form = b_form
		self.e_form = e_form
		self.soln = None
		self.num_operations = 0
		self.matrix = None

	def dot(self, matrix1, matrix2):
		# using definition of dot product: iterating over the rows of matrix1, multiplying
		# the ith entry of that row in matrix1 by the ith entry in matrix2, taking the sum,
		# and setting this value in the corresponding row of the solution matrix, 's'
		s = np.zeros(self.dim)
		for row in range(len(matrix1)):
			s[row] = sum(mat1_i*mat2_i for mat1_i,mat2_i in \
					zip(matrix1[row], matrix2))
			self.num_operations += self.dim + 1
		return s

	def build_matrix(self):
		#	Building the sparse matrix: filled in the d, a, b, e arrays
		#	using the formulas, then made d, a, and b into sparse
		#	diagonal matrices and added those together. Then changed
		# 	the last column in this matrix to have the values of e in
		#	its first n-2 rows.
		for i in range(len(self.d)):
			self.d[i] = self.d_form(i)
			self.num_operations += 1
		for i in range(len(self.a)):
			self.a[i] = self.a_form(i)
			self.b[i] = self.b_form(i)
			self.num_operations += 2
		for i in range(len(self.e)):
			self.e[i] = self.e_form(i)
			self.num_operations += 1
		d_mat = diags(self.d, 0).toarray()
		a_mat = diags(self.a, 1).toarray()
		b_mat = diags(self.b, -1).toarray()
		mat = d_mat + a_mat + b_mat
		mat[:, self.dim-1][:len(self.e)] = self.e
		self.num_operations += 5
		return mat

	def mult(self, matrix2):
		#	built C, took the dot product of C and Y, and set this as the 
		#	solution to the equation
		self.matrix = self.build_matrix()
		print('y: \n', matrix2)
		print('C: \n', self.matrix)
		self.soln = self.dot(self.matrix, matrix2).reshape((self.dim, 1))
		print('r: \n', self.soln)
		return self.soln

	def solve_helper(self, matrix, soln):
		# changing the first entry to 1
		a = matrix[0][0]
		matrix[0][0] = 1
		for j in range(1, len(matrix)):
			# multiplying elements of first row by 1/a if they're non-zero
			if j <= 1 or j == len(matrix)-1:
				matrix[0][j] = matrix[0][j]*(1/a)
				self.num_operations += 1
		# multiplying first row in solution vector by 1/a
		soln[0][0] = soln[0][0]*(1/a)
		self.num_operations += 1
		if 0 < len(matrix) - 1:
			# setting second row's first column to 0
			factor = matrix[1][0]
			for j in range(len(matrix)):
				# subtracting factor*above value from the jth entry in the 2nd row if it's non-zero
				if abs(1-j) <= 1 or j == len(matrix)-1:
					matrix[1][j] -= matrix[0][j]*factor
					self.num_operations += 1
			# applying same change to 2nd row in solution vector
			soln[1][0] -= soln[0]*factor
			self.num_operations += 1
		return matrix, soln

	def solve(self):
		mat = np.zeros((self.dim, self.dim))
		soln = np.zeros((self.dim, 1)).reshape((self.dim, 1))
		for i in range(self.dim):
			# iterating over the number of rows, going from nxn to 1x1 matrices, 
			# then adding the simplified matrix to the nxn zero matrix 'mat' and 
			# adding the simplified solution matrix to the nx1 zero matrix 'soln'
			mat[i:, i:], soln[i:] = self.solve_helper(self.matrix[i:, i:], self.soln[i:])
		# back solve
		x = np.zeros(5).reshape((5, 1))
		for i in range(self.dim-1, -1, -1):
			x[i] = soln[i]
			for j in range(i+1, self.dim):
				x[i] -= mat[i][j]*x[j]
				self.num_operations += self.dim - (i+1)
		return x

		
if __name__=='__main__':
	start = time.time()
	d_formula = lambda k: 4 + 0.1*k
	a_formula = lambda k: 1 + 0.01*(k**2)
	b_formula = lambda k: 1 - 0.01 - 0.03*k
	e_formula = lambda k: 1 - 0.05*k
	y = np.array([1, 2, 3, 4, 5]).reshape((5,1))
	edge_tri = Edge_Tridiag(5, d_formula, a_formula, b_formula, e_formula)
	edge_tri.mult(y)
	print('x: \n', edge_tri.solve())
	end = time.time()
	run = end-start

	print('Number of operations for 5x5: ', edge_tri.num_operations, '\n')
	print('time to solve 5x5: ', run, '\n')
	print('Number of operations for 40000x40000: ', 42670666860000, '\n')
	print('Ratio between number of operations: ', 251003922705.88235, '\n')
	t = run*251003922705.88235
	print('Estimated time to solve 40000x40000: ', t, ' seconds or ', t/60, ' minutes or ', \
			t/60/60, ' hours\n')








