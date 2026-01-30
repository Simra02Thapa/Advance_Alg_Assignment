"""
Multithreaded Merge Sort Algorithm
Uses QuickSort for sorting halves and Merge for combining results.
Three threads: 2 for sorting, 1 for merging with synchronization.
"""

import threading


class MultithreadedMergeSort:
    """Implements parallel merge sort using 3 threads."""
    
    def __init__(self):
        self.left_half = []
        self.right_half = []
        self.sorted_result = []
        self.thread_left = None
        self.thread_right = None
        self.lock = threading.Lock()
    
    # QUICKSORT ALGORITHM 
    
    def quicksort(self, arr, low, high):
        """
        QuickSort to sort array in-place.
        Time Complexity: O(n log n) average case
        """
        if low < high:
            pivot_index = self._partition(arr, low, high)
            self.quicksort(arr, low, pivot_index - 1)
            self.quicksort(arr, pivot_index + 1, high)
    
    def _partition(self, arr, low, high):
        """Lomuto partition scheme."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    # THREAD FUNCTIONS 
    
    def sort_left_half(self):
        """Thread 1: Sort left half using QuickSort."""
        print(f"Thread Left: Sorting {self.left_half}")
        self.quicksort(self.left_half, 0, len(self.left_half) - 1)
        print(f"Thread Left: Completed -> {self.left_half}")
    
    def sort_right_half(self):
        """Thread 2: Sort right half using QuickSort."""
        print(f"Thread Right: Sorting {self.right_half}")
        self.quicksort(self.right_half, 0, len(self.right_half) - 1)
        print(f"Thread Right: Completed -> {self.right_half}")
    
    def merge_sorted_halves(self):
        """Thread 3: Wait for sorting threads and merge results."""
        # Wait for both sorting threads to complete
        print("Thread Merge: Waiting for sorting threads...")
        self.thread_left.join()
        self.thread_right.join()
        print("Thread Merge: Both threads completed, starting merge...")
        
        # Merge two sorted arrays
        i, j = 0, 0
        merged = []
        
        while i < len(self.left_half) and j < len(self.right_half):
            if self.left_half[i] <= self.right_half[j]:
                merged.append(self.left_half[i])
                i += 1
            else:
                merged.append(self.right_half[j])
                j += 1
        
        # Append remaining elements
        merged.extend(self.left_half[i:])
        merged.extend(self.right_half[j:])
        
        with self.lock:
            self.sorted_result = merged
        
        print(f"Thread Merge: Completed -> {self.sorted_result}")
    
    # MAIN SORT FUNCTION 
    
    def sort(self, data):
        """
        Main function to perform multithreaded merge sort.
        
        Args:
            data: List of integers to sort
            
        Returns:
            Sorted list
        """
        print(f"\n{'='*60}")
        print(f"Input Array: {data}")
        print(f"{'='*60}")
        
        # Step 1: Divide array into two halves
        mid = len(data) // 2
        self.left_half = data[:mid].copy()
        self.right_half = data[mid:].copy()
        
        print(f"\nStep 1 - DIVIDE:")
        print(f"  Left Half:  {self.left_half}")
        print(f"  Right Half: {self.right_half}")
        
        # Step 2: Create threads
        print(f"\nStep 2 - CREATE THREADS:")
        self.thread_left = threading.Thread(target=self.sort_left_half)
        self.thread_right = threading.Thread(target=self.sort_right_half)
        thread_merge = threading.Thread(target=self.merge_sorted_halves)
        
        # Step 3: Start sorting threads in parallel
        print("\nStep 3 - START PARALLEL SORTING:")
        self.thread_left.start()
        self.thread_right.start()
        
        # Step 4: Start merge thread (waits for sorting threads)
        thread_merge.start()
        
        # Step 5: Wait for merge to complete
        thread_merge.join()
        
        print(f"\n{'='*60}")
        print(f"FINAL SORTED ARRAY: {self.sorted_result}")
        print(f"{'='*60}\n")
        
        return self.sorted_result


# MAIN EXECUTION 

if __name__ == "__main__":
    # Example usage
    sorter = MultithreadedMergeSort()
    
    # Test data
    test_array = [47, 65, 40, 16, 82, 53, 56, 66, 38, 99, 10, 70, 14, 48, 100, 35, 20, 14, 5, 78]
    
    # Perform sort
    result = sorter.sort(test_array)
    
    # Verify result
    print(f"Original: {test_array}")
    print(f"Sorted:   {result}")
    print(f"Correct:  {result == sorted(test_array)}")
