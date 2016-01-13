class Solution:
	# @param {character[][]} grid
	# @return {integer}
	def numIslands(self, grid):
		numrows = len(grid)
		if numrows == 0:
			return 0

		numcols = len(grid[0])
		if numcols == 0:
			return 0

		islands = 0
		for i in range(numrows):
			for j in range(numcols):
				#print "(i,j) = (%s, %s)" % (str(i), str(j))
				if grid[i][j] == "1":
					islands = islands + 1
					self.combIsland(i, j, grid, numrows, numcols)
		return islands

	# @param {integer} x
	# @param {integer} y
	# @param {char[][]} grid
	# @param {integer} numrows
	# @param {integer} numcols
	def combIsland(self, x, y, grid, numrows, numcols):
		if((y < 0) or (x < 0) or (y >= numcols) or (x >= numrows) or grid[x][y] == "0"):
			return
		else:
			grid[x][y] = "0"

			# North 
			self.combIsland((x-1), y, grid, numrows, numcols)

			# East 
			self.combIsland(x, (y+1), grid, numrows, numcols)

			# South
			self.combIsland((x+1), y, grid, numrows, numcols)

			# West 
			self.combIsland(x, (y-1), grid, numrows, numcols)