import math

def get_distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_total_distance(hub, sensors):
    """Calculate the sum of distances from the hub to all sensors."""
    total_dist = 0
    for sensor in sensors:
        total_dist += get_distance(hub, sensor)
    return total_dist

def solve_optimal_hub_placement(sensor_locations):
    # Step 1: Start with a "Guess". 
    # The centroid (average x, average y) is a great starting point.
    sum_x = sum(s[0] for s in sensor_locations)
    sum_y = sum(s[1] for s in sensor_locations)
    n = len(sensor_locations)
    
    # Current best guess for Hub [x, y]
    hub = [sum_x / n, sum_y / n]

    # Step 2: Iteratively refine the position (Weiszfeld's Algorithm Approach)
    # loop until the hub stops moving significantly.
    learning_rate = 1.0  
    precision = 0.0000001 
    
    # Here, we use a simpler Gradient Descent style which is easier to understand and debug.
    
    max_iterations = 1000
    for _ in range(max_iterations):
        current_x, current_y = hub
        
        # Calculate the "pull" from each sensor
        numerator_x = 0
        numerator_y = 0
        denominator = 0
        
        can_calculate = True
        
        for sensor in sensor_locations:
            dist = get_distance(hub, sensor)
            
            if dist == 0: 
                dist = 0.000000001 
                
            weight = 1.0 / dist
            
            numerator_x += sensor[0] * weight
            numerator_y += sensor[1] * weight
            denominator += weight

        # Calculate the new candidate position
        new_x = numerator_x / denominator
        new_y = numerator_y / denominator
        
        shift_dist = get_distance(hub, [new_x, new_y])
        
        hub = [new_x, new_y]
        
        if shift_dist < precision:
            break
    min_total_sum = calculate_total_distance(hub, sensor_locations)
    return min_total_sum

# Testing with Assignment Examples

# Example 1
sensors_1 = [[0,1], [1,0], [1,2], [2,1]]
result_1 = solve_optimal_hub_placement(sensors_1)
print(f"Example 1 Output: {result_1:.5f}") 

# Example 2
sensors_2 = [[1,1], [3,3]]
result_2 = solve_optimal_hub_placement(sensors_2)
print(f"Example 2 Output: {result_2:.5f}") 

# some more points as Example
sensors_3 = [[0,0], [1,0], [-1,0], [0,1], [0,-1]]
print(f"Example 3 Output: {solve_optimal_hub_placement(sensors_3):.5f}") 

#some more points as Example 
sensors_4 = [[0,0], [0,2], [2,0], [2,2]]
print(f"Example 4 Output: {solve_optimal_hub_placement(sensors_4):.5f}")