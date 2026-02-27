import numpy
import plotly_express as plt
import json

def calculate_after_tax_income(income, state_code, marital_status, data_file='tax_brackets_2025.json'):
    #load tax code
    with open(data_file, 'r') as f:
        data = json.load(f)

    year = "2025"
    marital_status = marital_status.lower()  # 'single' or 'married'

    def get_tax_owed(taxable_income, brackets):
        if taxable_income <= 0:
            return 0

        tax_owed = 0
        for i, bracket in enumerate(brackets):
            b_min = bracket['min']
            b_max = bracket['max']
            rate = bracket['rate']

            if b_max is None or taxable_income < b_max:
                # Income falls within or ends in this bracket
                tax_owed += (taxable_income - b_min) * rate
                break
            else:
                # Income exceeds this bracket; tax the full range
                tax_owed += (b_max - b_min) * rate
        return tax_owed

    # --- Federal Calculation ---
    fed_deduction = data['standardDeductions'][year]['federal'][marital_status]
    fed_taxable = max(0, income - fed_deduction)
    fed_brackets = data['taxBrackets'][year]['federal'][marital_status]
    fed_tax = get_tax_owed(fed_taxable, fed_brackets)

    # --- State Calculation ---
    state_tax = 0
    if state_code in data['taxBrackets'][year]:
        # Handle states with no income tax (like FL)
        state_brackets = data['taxBrackets'][year][state_code][marital_status]

        if state_brackets:  # Only if the list isn't empty
            state_deduction = data['standardDeductions'][year].get(state_code, {}).get(marital_status, 0)
            state_taxable = max(0, income - state_deduction)
            state_tax = get_tax_owed(state_taxable, state_brackets)

    # --- Final Result ---
    total_tax = fed_tax + state_tax
    return round(income - total_tax, 2)

def essentialSpending():

    return 1

class individual:
    def __init__(self, age, gender, income, location, marital_status, risk_tolerance):
        self.age = age
        self.gender = gender
        self.income = income
        self.location = location
        self.risk_tolerance = risk_tolerance
        self.income_after_tax = calculate_after_tax_income(income, location, marital_status)
