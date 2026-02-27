import numpy as np
import math

def k_from_tolerance(t):
    # Logistic curve for smooth, realistic growth of k
    min_k = 0.01      # minimum share of income spent
    max_k = 1.2      # maximum share of income spent
    steepness = 6     # controls how sharply k increases around t=0.5

    # Logistic function
    logistic = 1 / (1 + math.exp(-steepness * (t - 0.5)))

    # Scale logistic output into [min_k, max_k]
    return min_k + (max_k - min_k) * logistic

def daily_gambling_spend(income, tolerance):
    income = income/365
    # k now comes from logistic curve
    k = k_from_tolerance(tolerance)


    # Mean daily spend
    mean = k * income
    print(f"mean is {mean}")

    # Standard deviation proportional to mean
    std = mean * 0.4

    # Sample from normal distribution
    spend = np.random.normal(loc=mean, scale=std)

    # Prevent negative values
    amount = max(0, spend)
    return round(amount, 2)

