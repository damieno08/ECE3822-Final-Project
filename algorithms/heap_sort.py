def heapify_games(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left].game_name > arr[largest].game_name:
        largest = left

    if right < n and arr[right].game_name > arr[largest].game_name:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_games(arr, n, largest)


def heap_sort_games(history):
    arr = history[:]
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify_games(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_games(arr, i, 0)

    return arr