import math
a, Ts, Rs, D, sigma = 0.306, 6.96e8, 6.96e6, 1.496e11, 1.2
print(f"The value of Tp is: {Ts * math.sqrt((Rs * math.sqrt((1 - a) / sigma)) / (2 * D))}")
