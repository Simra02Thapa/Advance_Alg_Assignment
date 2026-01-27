def fractional_knapsack(values, weights, capacity):
    items = []

    # Step 1: Compute ratios
    for i in range(len(values)):
        items.append((values[i] / weights[i], values[i], weights[i]))

    # Step 2: Sort by ratio descending
    items.sort(reverse=True)

    total_value = 0.0

    # Step 3: Pick items greedily
    for ratio, value, weight in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += value * (capacity / weight)
            break

    return total_value


values = [12, 10, 20, 15, 2, 3, 50]
weights = [2, 1, 3, 2, 12, 10, 1]
capacity = 15

print("Maximum loot:", fractional_knapsack(values, weights, capacity))