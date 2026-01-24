def strategic_tile_shatter(tile_multipliers):
    # Add boundary tiles with value 1
    arr = [1] + tile_multipliers + [1]
    n = len(arr)

    # Create DP table
    dp = [[0 for _ in range(n)] for _ in range(n)]

    # Interval DP
    for length in range(2, n):                    
        for left in range(0, n - length):
            right = left + length

            for k in range(left + 1, right):       
                points = (
                    dp[left][k] +
                    dp[k][right] +
                    arr[left] * arr[k] * arr[right]
                )
                dp[left][right] = max(dp[left][right], points)

            print(f"dp[{left}][{right}] = {dp[left][right]}")
        print("-" * 50)

    return dp[0][n - 1]


# Example 1 
tiles1 = [3, 1, 5, 8]
print("Example 1 Tiles:", tiles1)
print("Maximum Points:", strategic_tile_shatter(tiles1))
print("=" * 60)

# Example 2-
tiles2 = [1, 5]
print("Example 2 Tiles:", tiles2)
print("Maximum Points:", strategic_tile_shatter(tiles2))
print("=" * 60)

# Example 3 (additional eg.)
tiles3 = [2, 4, 3]
print("Example 3 Tiles:", tiles3)
print("Maximum Points:", strategic_tile_shatter(tiles3))
