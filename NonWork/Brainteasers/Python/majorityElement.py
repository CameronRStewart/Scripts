# Given an array of size n, find the majority element. 
# The majority element is the element that appears more than ⌊ n/2 ⌋ times.

class Solution:
    # @param num, a list of integers
    # @return an integer
    def majorityElement(self, num):
        count = len(num)
        di = dict()
        
        for n in num:
            if count <= 1:
                return n
            if n in di:
                di[n] += 1
                if di[n] >= count/2:
                    return n
            else:
                di[n] = 0