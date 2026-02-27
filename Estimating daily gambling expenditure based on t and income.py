import numpy as np
import math

def k_from_tolerance(t):
    # Logistic curve for smooth, realistic growth of k
    min_k = 0.01      # minimum share of income spent
    max_k = 0.12      # maximum share of income spent
    steepness = 6     # controls how sharply k increases around t=0.5

    # Logistic function
    logistic = 1 / (1 + math.exp(-steepness * (t - 0.5)))

    # Scale logistic output into [min_k, max_k]
    return min_k + (max_k - min_k) * logistic

def daily_gambling_spend(income, tolerance):
    # k now comes from logistic curve
    k = k_from_tolerance(tolerance)

    # Mean daily spend
    mean = k * income

    # Standard deviation proportional to mean
    std = mean * 0.3

    # Sample from normal distribution
    spend = np.random.normal(loc=mean, scale=std)

    # Prevent negative values
    return max(0, spend)

# Example usage
income = float(input("Enter income: "))/365
tolerance = float(input("Enter gambling tolerance (0–1): "))

amount = daily_gambling_spend(income, tolerance)
print("Estimated gambling spend today:", round(amount, 2))
