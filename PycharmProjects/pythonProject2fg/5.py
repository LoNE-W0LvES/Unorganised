
h = int(input("Enter the initial height (in meters): "))
n = int(input("Enter the number of bounces (n): "))

if n > 0:
    t_d = 0
    for i in range(n):
        t_d += h
        h /= 2
    print(f"Total distance traversed after {n} bounces: {t_d:.2f} meters")
