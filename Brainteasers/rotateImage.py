class Solution:
    # @param {integer[][]} matrix
    # @return {void} Do not return anything, modify matrix in-place instead.
	def rotate(self, matrix):

		matrix_size = len(matrix)

		if (matrix_size == 1):
			return

		i = 0
		count = matrix_size - 1
		first = True
		while i < count:
			self.swap(matrix, 0, i, 0, i, first)
			i = i+1

		return matrix

	def swap(self, matrix, x, y, x_prime, y_prime, first):
		if(((x,y) == (x_prime, y_prime)) and not(first) ):
			return
		else:
			matrix_size = len(matrix)
			tmpx = y
			tmpy = matrix_size - x

			self.swap(matrix, tmpx, tmpy, x_prime, y_prime)
			matrix[tmpx][tmpy] = matrix[x][y]
			return