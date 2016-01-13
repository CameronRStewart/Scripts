class LRUCache:

	# @param capacity, an integer
	def __init__(self, capacity):
		self.capacity = capacity
		# Total number of cached items for this list.
		self.listCount = 0
		# CacheNode pointer to the first item (MRU)
		self.head = None
		# CacheNode pointer to the last item (LRU)
		self.tail = None
		# map variable to do searches with
		self.map = {}

	# @param key, untyped
	# @return an integer
	def get(self, key):

		if key in self.map:
			value = self.map[key].value
			self.pop(self.map[key])
			self.set(key, value)
			return value
		else:
			return -1

	# @param key, an integer
	# @param value, an integer
	# @return nothing
	def set(self, key, value):

		if key in self.map:
			self.pop(self.map[key])

		if (self.listCount >= self.capacity):
			self.pop(self.tail)
			self.set(key, value)
		else:

			new = CacheNode(key, value)

			if self.listCount <= 0:
				self.head = new
				self.tail = new
				new.last = None
				new.next = None
			else:	
				old_head = self.head
				new.next = self.head
				# Unneccesary, but just to be safe
				new.last = None
				old_head.last = new
				self.head = new

			self.map[key] = new
			self.listCount = self.listCount + 1

	# @param node, CacheNode
	# @return, nothing 
	# Not a true pop, more of a delete.
	def pop(self, node):

		if (node.last == None and node.next == None):
			# Only element
			self.head = None
			self.tail = None
		elif (node.next == None):
			# Tail
			node.last.next = None
			self.tail = node.last
		elif (node.last == None):
			# Head
			node.next.last = None
			self.head = node.next
		else:
			node.last.next = node.next
			node.next.last = node.last


		del self.map[node.key]
		del node
		self.listCount = self.listCount - 1

	# This is a function designed to procure output
	# of the results of your operations.
	def printCache(self):

		cur = self.head
		while (not(cur == None)):
			print "(%s, %s)" % (cur.key, cur.value)
			cur = cur.next



class CacheNode:

	# @param key, untyped (string, int, etc)
	# @param value, int
	def __init__(self, key, value):
		self.last = None
		self.next = None
		self.key = key
		self.value = value