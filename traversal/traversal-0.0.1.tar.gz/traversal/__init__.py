import sys

def zigzag(rows, columns, matrix):

    solution = [[] for i in range(rows + columns - 1)]

    for i in range(rows):
        for j in range(columns):
            sum = i + j
            if(sum % 2 == 0):
                solution[sum].insert(0, matrix[i][j])
            else:
                solution[sum].append(matrix[i][j])

    for i in solution:
        for j in i:
            print(j, end=' ')

# matrix = [[[] for i in range(rows)] for i in range(columns)]