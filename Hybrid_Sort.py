import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def generate_random_data(size):
    # Generate a list of unique positive integers within the specified range
    data = random.sample(range(1, size * 10), size)
    return data

def remove_duplicates_and_negatives(data):
    # Remove duplicates and negative numbers from the dataset
    unique_positive_data = set()
    for num in data:
        if num > 0:
            unique_positive_data.add(num)
    return list(unique_positive_data)

def bubble_sort(data):
    n = len(data)
    for i in range(n):
        # Initialize a flag to track if any swaps occurred during the pass
        swapped = False
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
        # If no swaps occurred, the array is already sorted, break out of the loop
        if not swapped:
            break

def quick_sort(data):
    if len(data) <= 1:
        return data
    else:
        # Use median-of-three pivot selection method
        mid = len(data) // 2
        pivot_values = [data[0], data[mid], data[-1]]
        pivot_value = sorted(pivot_values)[1]  # Median of the three
        left = [x for x in data if x < pivot_value]
        middle = [x for x in data if x == pivot_value]
        right = [x for x in data if x > pivot_value]
        return quick_sort(left) + middle + quick_sort(right)

def merge_sort(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        # Create a single auxiliary array once and reuse it for all merges
        merged_data = [0] * len(data)
        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                merged_data[k] = left_half[i]
                i += 1
            else:
                merged_data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            merged_data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            merged_data[k] = right_half[j]
            j += 1
            k += 1

        # Copy merged data back to the original data list
        data[:] = merged_data

def hybrid_sort(data, threshold_bubble, threshold_quick):
    if len(data) <= threshold_bubble:
        return bubble_sort(data)
    elif len(data) <= threshold_quick:
        return quick_sort(data)
    else:
        return merge_sort(data)

def measure_time(sort_function, data, threshold_bubble, threshold_quick):
    start_time = time.time()
    sorted_data = data.copy()
    sort_function(sorted_data, threshold_bubble, threshold_quick)
    end_time = time.time()
    return sorted_data, end_time - start_time

# User inputs
num_datasets = int(input("Enter the number of datasets: "))
dataset_sizes = []
for i in range(num_datasets):
    size = int(input(f"Enter the size of dataset {i+1}: "))
    dataset_sizes.append(size)

# Varying threshold values for Bubble Sort and Quick Sort
threshold_bubble_values = [10, 50, 100, 150, 200]
threshold_quick_values = [1000, 3000, 5000, 7000, 10000]

# Dictionary to store time complexity data for each combination of threshold values
time_complexity_data = {}

# Create a DataFrame to store time complexity data
data_columns = [f'Dataset_{size}' for size in dataset_sizes]
df = pd.DataFrame(columns=data_columns)

data_columns = [f'Dataset_{size}' for size in dataset_sizes]
master_df = pd.DataFrame(columns=data_columns)

# Loop over different threshold values for Bubble Sort and Quick Sort
for threshold_bubble in threshold_bubble_values:
    for threshold_quick in threshold_quick_values:
        # Sort multiple datasets and measure the time taken
        time_taken = []
        for i in range(num_datasets):
            dataset = generate_random_data(dataset_sizes[i])
            positive_data = remove_duplicates_and_negatives(dataset)
            _, time_elapsed = measure_time(hybrid_sort, positive_data.copy(), threshold_bubble, threshold_quick)
            time_taken.append(time_elapsed)

        # Store time complexity data for the current combination of thresholds
        key = f"Threshold_Bubble_{threshold_bubble}_Threshold_Quick_{threshold_quick}"
        time_complexity_data[key] = time_taken

        # Add the time complexity data to the master DataFrame
        master_df.loc[key] = time_taken

# Display the master DataFrame as a single combined table
print("Combined Time Complexity Table:")
print(master_df)