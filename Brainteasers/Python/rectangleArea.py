class Solution:
    # @param {integer} A
    # @param {integer} B
    # @param {integer} C
    # @param {integer} D
    # @param {integer} E
    # @param {integer} F
    # @param {integer} G
    # @param {integer} H
    # @return {integer}
    def computeArea(self, A, B, C, D, E, F, G, H):
        intersect_length = self.findIntersectionVector(A, C, E, G)
        intersect_width = self.findIntersectionVector(B, D, F, H)
        intersect_area = (intersect_length * intersect_width)
        total = self.computeSingleArea(A, B, C, D) + self.computeSingleArea(E, F, G, H) - intersect_area
        return total


    def findIntersectionVector(self, point1, point2, point3, point4):
        # Mapping of points in plane:
        # X1/Y1 = A/B = point1
        # X2/Y2 = C/D = point2
        # X3/Y3 = E/F = point3
        # X4/Y4 = G/H = point4

        # Test for no intersection
        if((point2 <= point3) or (point4 <= point1)):
            return 0
        if (point1 < point3):
            intersect_point1 = point3
        else:
            intersect_point1 = point1
        if (point4 < point2):
            intersect_point2 = point4
        else:
            intersect_point2 = point2

        return intersect_point1 - intersect_point2

        

    def computeSingleArea(self, X1, Y1, X2, Y2):
        result = abs((X2 - X1) * (Y2 - Y1))
        return result