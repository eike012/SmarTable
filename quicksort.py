# Our compare function
def compare(a, b):
    if a[1][0] > b[1][0]: return 1
    elif a[1][0] < b[1][0]: return 0
    elif a[0][0] > b[0][0]: return 1
    else: return 1

# Partition function
def partition(array, low, high):
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if compare(pivot, array[j]):

            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
 
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 

    return i + 1
 
# Function to perform quicksort
def quickSort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quickSort(array, low, pi - 1)
        quickSort(array, pi + 1, high)