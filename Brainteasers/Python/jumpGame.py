class Solution:
    # @param {integer[]} nums
    # @return {boolean}
    def canJump(self, nums):
		if (len(nums) == 1):
			return True
		else:
			result_array = []
			for i in range(len(nums)):
				result_array.append(None)
			return self.canJumpFromHere(0, nums, result_array)

    def canJumpFromHere(self, index, nums, result_array):
		# The final index, the goal

		#print "Index: %s" % index

		if(not(result_array[index] == None)):
			return result_array[index]

		final_index = len(nums) - 1

		if(index == final_index):
			return True
		elif(index > final_index):
			return False
		elif((index < final_index) and (nums[index] == 0)):
			return False
		else:
			max_jump = nums[index]
			max_index = index + max_jump

			i = index + 1
			logic = False

			while (i <= max_index):
				#return False or self.canJumpFromHere(i, nums)
				logic = logic or self.canJumpFromHere(i, nums, result_array)
				i = i + 1

			result_array[index] = logic
			return logic