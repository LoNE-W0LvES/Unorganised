def find_saddle_point(matrix, matrix_t):
    for i in range(len(matrix)):
        gx = matrix[i].index(min(matrix[i]))
        gz = matrix_t[i].index(max(matrix_t[i]))
        if matrix[i][gx] == matrix_t[i][gz]:
            return [matrix[i][gx], gx, gz]
    return False


if __name__ == '__main__':
    mX = int(input("Enter the number of rows and columns: "))
    mat = []
    print("Enter the elements of the matrix:")
    for x in range(mX):
        row = input().split(' ')
        n_r = [int(i) for i in row]
        mat.append(n_r)
    mat_t = [[mat[i][j] for i in range(mX)] for j in range(mX)]
    s_p = find_saddle_point(mat, mat_t)
    print(f"{str(s_p[0])} is the saddle point at ({s_p[1] + 1}, {s_p[2] + 1})" if s_p else "No Saddle Point.")
