# Given two integers representing the numerator and denominator of a fraction, 
# return the fraction in string format.
# If the fractional part is repeating, enclose the repeating part in parentheses.

class Solution:
    # @return a string
    def fractionToDecimal(self, numerator, denominator):
        (integer, remainder) = divmod(numerator, denominator)
        if remainder == 0:
            return str(integer)
        else:
            return str(integer) + '.' + self.tenths(remainder, denominator, '')
            
    def tenths(self, numerator, denominator, history):
        if denominator == 10:
            return history + str(numerator)
        else:
            (integer, remainder) = divmod((10 * numerator), denominator)
            if remainder == 0:
                return history + str(integer)
            elif (remainder, denominator) == (numerator, denominator):
                return history + '(' + str(integer) + ')'
            elif str(integer) in history:
                repeating = history.index(str(integer))
                return history[:repeating] + '(' + history[repeating:] + ')'
            else:
                return self.tenths(remainder, denominator, history + str(integer))