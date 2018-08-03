def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = mergesort(arr[:mid]), mergesort(arr[mid:])

    return merge(left, right, arr.copy())


def merge(left, right, merged):
    leftCursor, rightCursor = 0, 0
    while leftCursor < len(left) and rightCursor < len(right):
        if left[leftCursor] <= right[rightCursor]:
            merged[leftCursor+rightCursor]=left[leftCursor]
            leftCursor += 1
        else:
            merged[leftCursor + rightCursor] = right[rightCursor]
            rightCursor += 1
    for leftCursor in range(leftCursor, len(left)):
        merged[leftCursor + rightCursor] = left[leftCursor]
    for rightCursor in range(rightCursor, len(right)):
        merged[leftCursor + rightCursor] = right[rightCursor]

    return merged
