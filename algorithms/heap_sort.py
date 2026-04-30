class HeapSortGames:
    def heapify(self, arr, n, i, mode):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        def get_value(obj):
            if mode == "time":
                # Check for GameSession (start_time) or ChatMessage (timestamp)
                return getattr(obj, 'start_time', getattr(obj, 'timestamp', 0))
            return getattr(obj, 'score', 0)

        if l < n and get_value(arr[l]) > get_value(arr[largest]):
            largest = l
        if r < n and get_value(arr[r]) > get_value(arr[largest]):
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.heapify(arr, n, largest, mode)

    def heap_sort(self, arr, mode="time"):
        n = len(arr)
        if n < 2: return arr
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i, mode)
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self.heapify(arr, i, 0, mode)
        return arr