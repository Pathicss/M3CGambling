# Gambling expenditure model based on income elasticity
# Every 10% increase in income -> 5% increase in gambling expenditure

import math

# Baseline values (you can adjust these)
MEDIAN_INCOME = 150000
BASE_EXPENDITURE = 6000  # expected gambling expenditure at median income

# Elasticity derived from 10% income -> 5% expenditure
ELASTICITY = math.log(1.05) / math.log(1.10)

def expected_gambling_expenditure(income):
    ratio = income / MEDIAN_INCOME
    return BASE_EXPENDITURE * (ratio ** ELASTICITY)

# User input
income = float(input("Enter your household income: $"))
expenditure = expected_gambling_expenditure(income)

print(f"Expected annual gambling expenditure: ${expenditure:.2f}")