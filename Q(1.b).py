import math
import random

#  UTILITY FUNCTIONS

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def total_distance(tour, cities):
    dist = 0
    for i in range(len(tour)):
        dist += distance(cities[tour[i]], cities[tour[(i+1) % len(tour)]])
    return dist

# NEIGHBOR OPERATIONS

def swap(tour):
    a, b = random.sample(range(len(tour)), 2)
    tour[a], tour[b] = tour[b], tour[a]

def two_opt(tour):
    a, b = sorted(random.sample(range(len(tour)), 2))
    tour[a:b] = reversed(tour[a:b])

# SIMULATED ANNEALING

def simulated_annealing(cities, cooling="exponential"):
    n = len(cities)
    current = list(range(n))
    random.shuffle(current)

    best = current[:]
    current_cost = total_distance(current, cities)
    best_cost = current_cost

    T = 1000
    T_min = 1e-3
    alpha = 0.995      # exponential
    beta = 0.5         # linear
    iteration = 0

    while T > T_min:
        new = current[:]

        if random.random() < 0.5:
            swap(new)
        else:
            two_opt(new)

        new_cost = total_distance(new, cities)
        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new
            current_cost = new_cost

            if current_cost < best_cost:
                best = current
                best_cost = current_cost

        iteration += 1
        if cooling == "exponential":
            T *= alpha
        else:
            T -= beta

    return best_cost


def generate_cities(n):
    return [(random.randint(0, 1000), random.randint(0, 1000)) for _ in range(n)]

cities = generate_cities(25)

print("Exponential Cooling Distance:", simulated_annealing(cities, "exponential"))
print("Linear Cooling Distance:", simulated_annealing(cities, "linear"))
