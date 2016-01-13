class Solution:
    # @param {integer[]} nums
    # @return {integer}
    def singleNumber(self, nums):
        nums.sort()
        count = 0
        last = None

        if len(nums) == 1:
            return nums[0]
        for i in nums:
            if (not(last == None) and not(last == i)):
                if count == 3:
                    last = i
                    count = 1
                elif count < 3:
                    return last
                else:
                    return i
        
            else:
                # last = i - incrememnt count
                last = i
                if count > 3:
                    return i
                count = count + 1
        return i
