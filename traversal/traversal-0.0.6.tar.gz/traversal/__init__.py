def zigzag(rows, columns, matrix):

    arr = []
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
            arr.append(j)

    print (arr)

def spiral(rows, columns, matrix) :
    k = 0; l = 0
    arr =[]
    while (k < rows and l < columns) :
        for i in range(l, columns) :
            arr.append(matrix[k][i])

        k += 1

        for i in range(k, rows) :
            arr.append(matrix[i][columns - 1])

        columns -= 1

        if ( k < rows) :

            for i in range(columns - 1, (l - 1), -1) :
                arr.append(matrix[rows - 1][i])

            rows -= 1

        if (l < columns) :
            for i in range(rows - 1, k - 1, -1) :
                arr.append(matrix[i][l])

            l += 1

    print (arr)

def row(rows, columns, matrix):
    mainarr = []
    for i in range(rows):
        arr = []
        for j in range(rows):
            arr.append(matrix[j][i])
        mainarr.append(arr)
    print (mainarr)


def column(rows, columns, matrix):
    mainarr = []
    for i in range(rows):
        arr = []
        for j in range(rows):
            arr.append(matrix[i][j])
        mainarr.append(arr)
    print (mainarr)


