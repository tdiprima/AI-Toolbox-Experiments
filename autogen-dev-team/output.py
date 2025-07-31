#---------------------
# QUICKSORT
def quicksort(array):
    if len(array) <= 1:
        return array
    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def test_quicksort():
    # Test case 1: Empty list
    assert quicksort([]) == []

    # Test case 2: Single element
    assert quicksort([1]) == [1]

    # Test case 3: Already sorted list
    assert quicksort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    # Test case 4: Reverse sorted list
    assert quicksort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    # Test case 5: Unsorted list with unique elements
    assert quicksort([3, 1, 4, 5, 2]) == [1, 2, 3, 4, 5]

    # Test case 6: List with duplicate elements
    assert quicksort([3, 1, 2, 3, 1]) == [1, 1, 2, 3, 3]

    # Test case 7: List with negative and positive integers
    assert quicksort([-1, -3, -2, 1, 2, 0]) == [-3, -2, -1, 0, 1, 2]

    # Test case 8: List with duplicate elements and negatives
    assert quicksort([-1, -3, -2, 1, -1, 2, -3]) == [-3, -3, -2, -1, -1, 1, 2]

    # Test case 9: Large list
    import random
    random_list = random.sample(range(1000), 100)
    assert quicksort(random_list) == sorted(random_list)

    print("All test cases pass")


# Run the test function
test_quicksort()
