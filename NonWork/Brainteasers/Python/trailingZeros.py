# Given an integer n, return the number of trailing zeroes in n!.
# Must be logarithmic time complexity.

class Solution:
    # @return an integer
    def trailingZeroes(self, n):
        if n < 5:
            return 0
        else:
            new_num = n // 5
            return new_num + self.trailingZeroes(new_num)