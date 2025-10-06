# quadratic_curve_fitter.py 
from  lib.quantity_pricing import QuantityPricing

class QuadraticCurveFitter:
    def __init__(self):
        self.a = 0.0
        self.b = 0.0
        self.c = 0.0

    def fit(self, points: list):
        if not points or len(points) == 0:
            raise ValueError("Points list cannot be null or empty.")
        
        # If only 2 points, do linear fitting
        if len(points) == 2:
            p1, p2 = points
            b = (p2.price - p1.price) / (p2.quantity - p1.quantity)
            c = p1.price - b * p1.quantity
            self.a = 0.0
            self.b = b
            self.c = c
            return

        n = len(points)
        sumX = sumX2 = sumX3 = sumX4 = 0.0
        sumY = sumXY = sumX2Y = 0.0

        for p in points:
            x = p.quantity
            y = p.price
            sumX += x
            sumX2 += x ** 2
            sumX3 += x ** 3
            sumX4 += x ** 4
            sumY += y
            sumXY += x * y
            sumX2Y += (x ** 2) * y

        matrix = [
            [n, sumX, sumX2],
            [sumX, sumX2, sumX3],
            [sumX2, sumX3, sumX4]
        ]

        vector = [sumY, sumXY, sumX2Y]

        c, b, a = self.solve(matrix, vector)
        self.a = a
        self.b = b
        self.c = c

    def predict(self, quantity: float) -> float:
        return self.a * (quantity ** 2) + self.b * quantity + self.c

    def solve(self, matrix: list, vector: list) -> list:
        n = len(vector)
        result = [0.0] * n

        # Forward elimination (Gaussian elimination)
        for i in range(n):
            for j in range(i + 1, n):
                ratio = matrix[j][i] / matrix[i][i]
                for k in range(i, n):
                    matrix[j][k] -= ratio * matrix[i][k]
                vector[j] -= ratio * vector[i]

        # Back substitution
        for i in range(n - 1, -1, -1):
            result[i] = vector[i]
            for j in range(i + 1, n):
                result[i] -= matrix[i][j] * result[j]
            result[i] /= matrix[i][i]

        return result
