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