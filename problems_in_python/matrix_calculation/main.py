matrix1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matrix2 = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
# addition fuction for matrices
def add_matrices(matrix1, matrix2):
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            result[i][j] = matrix1[i][j] + matrix2[i][j]
    return result

# subtraction function for matrices
def subtract_matrices(matrix1, matrix2):
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            result[i][j] = matrix1[i][j] - matrix2[i][j]
    return result

# multiplication function for matrices
def multiply_matrices(matrix1, matrix2):
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result

print("The addition of the matrices",add_matrices(matrix1, matrix2)) # [[10, 10, 10], [10, 10, 10], [10, 10, 10]]
print("The subtraction of the matrices",subtract_matrices(matrix1, matrix2)) # [[-8, -6, -4], [-2, 0, 2], [4, 6, 8]]
print("The multiplication of the matrices",multiply_matrices(matrix1, matrix2)) # [[30, 24, 18], [84, 69, 54], [138, 114, 90]]
