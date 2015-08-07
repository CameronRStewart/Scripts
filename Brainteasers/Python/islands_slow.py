# First stab at a solution, just for honesty (also using integer grid instead of string).
# This solution works, however it is far from optimal.  A better solution would be as follows:
# Where I decide to only check East and South of the current node, it would be better just to set counted nodes
# to 0, then check all neighbors on every node.  This would save me from needing most of the auxiliary functions
# in the Landmass class.


class Solution:
	# @param {integer[][]} grid
	# @return {integer}
	def numIslands(self, grid):

		numrows = len(grid)
		if numrows == 0:
			return 0

		numcols = len(grid[0])
		if numcols == 0:
			return 0

		x = 0
		y = 0

		landmasses = []

		while x < numrows:
			while y < numcols:
				for island in landmasses:
					if island.coordinateExists(x, y):
						y = island.getMaxYCoordinate(x) + 1
						break

				objective = Landmass()
				expedition_result = self.findLandmass(objective, grid, x, y, numrows, numcols)
				if expedition_result.size == 0:
					y = y + 1
					del objective
				else:
					landmasses.append(expedition_result)
					y = expedition_result.getMaxYCoordinate(x) + 1
			x = x + 1
			y = 0

		return len(landmasses)


	# @param {Landmass} mass
	# @param {character[][]} grid
	# @param {integer} x
	# @param {integer} y
	# @param {integer} numrows
	# @param {integer} numcols
	def findLandmass(self, mass, grid, x, y, numrows, numcols):

	
		if grid[x][y] == 0:
			return mass
		elif mass.coordinateExists(x,y):
			return mass
		else:
			mass.addLand(x, y)

			# The assumption is that we'll never need to
			# check neighbors to the North or West of us (since they likely called the function on us)
			# We will then check our neighbors to the East and South

			# East
			if (y+1) < numcols and grid[x][y+1] == 1:
				self.findLandmass(mass, grid, x, (y+1), numrows, numcols)
			
			# South
			if (x+1) < numrows and grid[x+1][y] == 1:
				self.findLandmass(mass, grid, (x+1), y, numrows, numcols)

			return mass





class Landmass:

	def __init__(self):
		# coordinates is an dictionary of arrays (coordinates).
		self.coordinates = {}
		self.size = 0

	# @param {integer} x
	# @param {integer} y
	def addLand(self, x, y):

		if x in self.coordinates:
			self.coordinates[x].append(y)
		else:
			self.coordinates[x] = [y]

		self.size = self.size + 1

	# @param {integer} x
	# @param {integer} y
	def coordinateExists(self, x, y):

		if x in self.coordinates and y in self.coordinates[x]:
			return True
		else:
			return False

	# @param {integer} x
	def getMaxYCoordinate(self, x):
		return max(self.coordinates[x])


