class Solution:
    # @param {integer[]} nums
    # @return {boolean}
	def canJump(self, nums):
		if (len(nums) == 1):
			return True
		else:
			return self.canJumpFromHere(0, nums)

	def canJumpFromHere(self, index, nums):
		final_index = len(nums) - 1

		max_jump = nums[index]
		max_index = index + max_jump

		logic = False

		if(index == final_index):
			return True
		elif((index < final_index) and (nums[index] == 0)):
			return False
		elif(index > final_index):
			return False
		else:
			i = index + 1
			while (i <= max_index):
				if (i == final_index):
					return True
				else:
					logic = False
					i = i+1
			return (logic or self.canJumpFromHere(index + 1, nums))
