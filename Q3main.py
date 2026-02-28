import numpy
import plotly_express as plt
import json

#tax
def calculate_after_tax_income(income, state_code, marital_status, data_file='tax_brackets_2025.json'):
    #load tax code
    with open(data_file, 'r') as f:
        data = json.load(f)

    year = "2025"
    marital_status = marital_status.lower()  # single or married

    def get_tax_owed(taxable_income, brackets):
        if taxable_income <= 0:
            return 0

        tax_owed = 0
        for i, bracket in enumerate(brackets):
            b_min = bracket['min']
            b_max = bracket['max']
            rate = bracket['rate']

            if b_max is None or taxable_income < b_max:
                tax_owed += (taxable_income - b_min) * rate
                break
            else:
                tax_owed += (b_max - b_min) * rate
        return tax_owed

    fed_deduction = data['standardDeductions'][year]['federal'][marital_status]
    fed_taxable = max(0, income - fed_deduction)
    fed_brackets = data['taxBrackets'][year]['federal'][marital_status]
    fed_tax = get_tax_owed(fed_taxable, fed_brackets)

    state_tax = 0
    if state_code in data['taxBrackets'][year]:
        state_brackets = data['taxBrackets'][year][state_code][marital_status]

        if state_brackets:
            state_deduction = data['standardDeductions'][year].get(state_code, {}).get(marital_status, 0)
            state_taxable = max(0, income - state_deduction)
            state_tax = get_tax_owed(state_taxable, state_brackets)

    total_tax = fed_tax + state_tax
    return round(income - total_tax, 2)

def life_hours_lost(income, state, marital_status, annual_work_hours, annual_gambling_loss, betting_sessions_per_week, minutes_per_session):

    netincome = calculate_after_tax_income(income, state, marital_status)
    hourly_wage = (netincome) / annual_work_hours
    work_hours_lost = annual_gambling_loss / hourly_wage
    gambling_hours = (52 * betting_sessions_per_week * minutes_per_session) / 60
    total_life_hours_lost = work_hours_lost + gambling_hours
    waking_hours_per_year = 16 * 365
    percent_life_lost = (total_life_hours_lost / waking_hours_per_year) * 100

    return percent_life_lost

print(round(life_hours_lost(
    income = 20000,
    state = "TN",
    marital_status = "single",
    annual_work_hours=2000,
    annual_gambling_loss=2000,
    betting_sessions_per_week=4,
    minutes_per_session=25),3))

# Profile: High Frequency / Low Individual Stakes
# Characterized by many short sessions throughout the week.
print(round(life_hours_lost(
    income = 45000,
    state = "TN",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 3500,
    betting_sessions_per_week = 14,
    minutes_per_session = 10), 3))

# Profile: High Ratio / Entry-Level Income
# Significant financial impact relative to a lower hourly wage.
print(round(life_hours_lost(
    income = 32000,
    state = "TN",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 4000,
    betting_sessions_per_week = 5,
    minutes_per_session = 30), 3))

# Profile: Extended Session / Median Income
# Characterized by fewer but much longer periods of engagement.
print(round(life_hours_lost(
    income = 65000,
    state = "TN",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 2500,
    betting_sessions_per_week = 3,
    minutes_per_session = 120), 3))

# Profile: Large-Scale Loss / High Income
# High absolute dollar loss requiring significant work hours to recover despite higher pay.
print(round(life_hours_lost(
    income = 140000,
    state = "TN",
    marital_status = "married",
    annual_work_hours = 2000,
    annual_gambling_loss = 18000,
    betting_sessions_per_week = 7,
    minutes_per_session = 45), 3))

# Profile: Pattern A (Higher Income in a High-Tax State)
# California's tax brackets will significantly lower the net hourly wage.
print(round(life_hours_lost(
    income = 120000,
    state = "CA",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 8000,
    betting_sessions_per_week = 5,
    minutes_per_session = 45), 3))

# Profile: Pattern B (Mid-Range Income in a Flat-Tax State)
# North Carolina (NC) typically uses a flat tax rate.
print(round(life_hours_lost(
    income = 52000,
    state = "NC",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 2500,
    betting_sessions_per_week = 3,
    minutes_per_session = 30), 3))

# Profile: Pattern C (Lower Income in a No-Tax State)
# Florida (FL) has no state income tax, maximizing the net hourly wage.
print(round(life_hours_lost(
    income = 30000,
    state = "FL",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 1500,
    betting_sessions_per_week = 10,
    minutes_per_session = 15), 3))

# Profile: Pattern D (High-Intensity Engagement in New York)
# New York (NY) has significant state and sometimes local taxes.
print(round(life_hours_lost(
    income = 85000,
    state = "NY",
    marital_status = "married",
    annual_work_hours = 2000,
    annual_gambling_loss = 5000,
    betting_sessions_per_week = 14,
    minutes_per_session = 20), 3))

# Profile: Pattern E (High Loss Ratio in Texas)
# Texas (TX) has no state income tax, but the loss amount is high relative to income.
print(round(life_hours_lost(
    income = 40000,
    state = "TX",
    marital_status = "single",
    annual_work_hours = 2000,
    annual_gambling_loss = 6000,
    betting_sessions_per_week = 4,
    minutes_per_session = 60), 3))