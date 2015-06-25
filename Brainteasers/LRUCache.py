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

	# @return an integer
	def get(self, key):
		# cur is a pointer to a CacheNode
		cur = self.head

		while (not(cur == None)):
			if (cur.key == key):
        		# Value found!  Push it to the front.

				# Maybe this ought to be called delete as it will
				# not return anything.
				value = cur.value
				key = cur.key
				self.pop(cur)
				self.set(key, value)
				return value

			else:
				cur = cur.next

		return -1

	# @param key, an integer
	# @param value, an integer
	# @return nothing
	def set(self, key, value):
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

			self.listCount = self.listCount + 1

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

		del node
		self.listCount = self.listCount - 1

	def printCache(self):

		cur = self.head
		while (not(cur == None)):
			print "(%s, %s)" % (cur.key, cur.value)
			cur = cur.next


class CacheNode:

	# @param value, integer
	def __init__(self, key, value):
		self.last = None
		self.next = None
		self.key = key
		self.value = value

#	def __eq__(self, node2):
#		if (self.key == node2.key and self.value == node2.value):
#			return True
#		else:
#			return False