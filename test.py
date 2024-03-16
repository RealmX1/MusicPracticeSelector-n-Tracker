import timeit

def remove_elements(original_list):
    while original_list:
        original_list.pop()

def construct_new_list(original_list):
    new_list = []
    for element in original_list:
        new_list.append(element)
    # Discard the old list
    del original_list

# Create a large list for testing
large_list = list(range(100000))

# Measure the time taken for each function
remove_time = timeit.timeit(lambda: remove_elements(large_list.copy()), number=1000)
construct_time = timeit.timeit(lambda: construct_new_list(large_list.copy()), number=1000)

print(f"Time to remove elements: {remove_time} seconds")
print(f"Time to construct new list: {construct_time} seconds")