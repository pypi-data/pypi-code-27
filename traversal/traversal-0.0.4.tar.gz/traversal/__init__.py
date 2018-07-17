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
    return ' '


def spiral(rows, columns, matrix) :
    k = 0; l = 0

    while (k < rows and l < columns) :
        for i in range(l, columns) :
            print(matrix[k][i], end = " ")

        k += 1

        for i in range(k, rows) :
            print(matrix[i][columns - 1], end = " ")

        columns -= 1

        if ( k < rows) :

            for i in range(columns - 1, (l - 1), -1) :
                print(matrix[rows - 1][i], end = " ")

            rows -= 1

        if (l < columns) :
            for i in range(rows - 1, k - 1, -1) :
                print(matrix[i][l], end = " ")

            l += 1
    return ' '

def row(rows, columns, matrix):
    for i in range(rows):
        for j in range(rows):
            print (matrix[j][i], end=' ')
    return ' '


def column(rows, columns, matrix):
    for i in range(rows):
        for j in range(rows):
            print (matrix[i][j], end=' ')
    return ' '