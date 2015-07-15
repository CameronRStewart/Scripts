# This problem asks that you rotate an n X n matrix 90 degrees in-place.
# I know that this problem is probably solved much more elegantly through sexier, more pythonic means,
# but this is the solution that I worked up.  Pretty ugly and needs a lot of work, but it works.


class Solution:
    # @param {integer[][]} matrix
    # @return {void} Do not return anything, modify matrix in-place instead.
	def rotate(self, matrix):
		self.submatrixRotate(matrix, 0)

		#print "Final Matrix: %s" % matrix
		return

	# @param {integer[][]} matrix
	# @param {integer} sub_iteration
	# @return {void}
	def submatrixRotate(self, matrix, sub_iteration):
		matrix_size = len(matrix)

		if (matrix_size == 1):
			return

		count = matrix_size - 1
		first = True
		i = sub_iteration
		j = sub_iteration

		while i < (count - sub_iteration):
			self.swap(matrix, j, i, j, i, first)
			i = i+1

		if (matrix_size - sub_iteration) > 3:
			sub_iteration = sub_iteration + 1

			self.submatrixRotate(matrix, sub_iteration)


		return

	# @param {integer[][]} matrix
	# @param {integer} x
	# @param {integer} y
	# @param {integer} x_prime
	# @param {integer} y_prime
	# @param {boolean} first
	# @return {void}
	def swap(self, matrix, x, y, x_prime, y_prime, first):
		if(((x,y) == (x_prime, y_prime)) and not(first) ):
			return
		else:
			matrix_size = len(matrix)
			tmpx = y
			tmpy = (matrix_size - x) - 1
			tmp_val = matrix[x][y]

			self.swap(matrix, tmpx, tmpy, x_prime, y_prime, False)
			matrix[tmpx][tmpy] = tmp_val
			return
