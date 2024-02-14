def is_symmetric(mat):
    size = len(mat)

    for r in mat:
        if len(r) != size:
            return False

    for i in range(size):
        for j in range(size):
            if mat[i][j] != mat[j][i]:
                return False
    return True


def print_matrix(m):
    for r in m:
        print(" ".join(map(str, r)))


n = int(input("Enter the number of rows and columns (n): "))
matrix = []

print("Enter the elements of the matrix:")
for x in range(n):
    row = input().split(' ')
    n_r = [int(i) for i in row]
    matrix.append(n_r)


if is_symmetric(matrix):
    print("\nThe matrix is symmetric.")
else:
    print("\nThe matrix is not symmetric.")
