"""
merge_sort.py - Generic merge sort implementation

Stable, O(n log n) worst-case sort. Accepts an optional key function and
reverse flag so it can sort any list of items by an arbitrary criterion.

Revision History:
    (ST) 04/25/2026 Create initial class
"""


def MergeSort(items, key=None, reverse=False):
    """
    Return a new sorted list. Does not modify the original.

    Args:
        items:   list-like sequence to sort
        key:     single-argument function applied to each element for comparison
        reverse: if True, sort descending (largest first)
    """
    lst = list(items)
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left  = MergeSort(lst[:mid],  key=key, reverse=reverse)
    right = MergeSort(lst[mid:],  key=key, reverse=reverse)
    return _merge(left, right, key, reverse)


def _merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        lv = key(left[i])  if key else left[i]
        rv = key(right[j]) if key else right[j]

        if (lv >= rv) if reverse else (lv <= rv):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
