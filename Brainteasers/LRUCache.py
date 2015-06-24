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

        while (not(cur == None)){
        	if (cur.value == key) {
        		# Value found!  Push it to the front.

        		# Maybe this ought to be called delete as it will
        		# not return anything.
        		new_front = self.pop(cur)
        		self.set(cur.key, cur.value)
        		return cur.value
        	}
        	else {
        		cur = cur.next
        	}
        }
        return -1

    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):


	def pop(self, node):
		tmp = node
		tmp.last.next = tmp.next
		tmp.next.last = tmp.last 

class CacheNode:

	# @param value, integer
	def __init__(self, key, value):
		self.last = None
		self.next = None
		self.key = key
		self.value = value