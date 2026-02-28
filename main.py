import numpy
import plotly_express as plt
import json
import random
from gamblingpropensity import get_gambling_decision
from daily_gambling_spending_estimate import daily_gambling_spend
from initial_t_value_calculator import getTolerance


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

# expenditures

ageEx = {
    "Under 25": 39138,
    "25-34": 60835,
    "35-44": 74968,
    "45-54": 77815,
    "55-64": 67735,
    "65-74": 57455,
    "75+": 51138
}
regionEx = {
    "Northeast": 68959,
    "Midwest": 59867,
    "South": 59108,
    "West": 75473
}
regionExAvg = sum(regionEx.values())/4
state_to_region = {
    # South
    "TN": "South", "AL": "South", "GA": "South", "FL": "South",
    "KY": "South", "MS": "South", "NC": "South", "SC": "South",
    "VA": "South", "WV": "South", "AR": "South", "LA": "South",
    "OK": "South", "TX": "South",

    # Northeast
    "ME": "Northeast", "NH": "Northeast", "VT": "Northeast",
    "MA": "Northeast", "RI": "Northeast", "CT": "Northeast",
    "NY": "Northeast", "NJ": "Northeast", "PA": "Northeast",

    # Midwest
    "OH": "Midwest", "MI": "Midwest", "IN": "Midwest",
    "IL": "Midwest", "WI": "Midwest", "MN": "Midwest",
    "IA": "Midwest", "MO": "Midwest", "ND": "Midwest",
    "SD": "Midwest", "NE": "Midwest", "KS": "Midwest",

    # West
    "CA": "West", "OR": "West", "WA": "West",
    "NV": "West", "AZ": "West", "UT": "West",
    "CO": "West", "NM": "West", "ID": "West",
    "MT": "West", "WY": "West", "AK": "West", "HI": "West"
}

def get_age_group(age):
    if age < 25:
        return "Under 25"
    elif age <= 34:
        return "25-34"
    elif age <= 44:
        return "35-44"
    elif age <= 54:
        return "45-54"
    elif age <= 64:
        return "55-64"
    elif age <= 74:
        return "65-74"
    else:
        return "75+"

def estimate_expenditure(age, state):
    state = state.upper()

    if state not in state_to_region:
        raise ValueError("Invalid state abbreviation.")

    region = state_to_region[state]
    age_group = get_age_group(age)

    base_spending = ageEx[age_group]
    region_ratio = regionEx[region] / regionExAvg
    adjusted_spending = base_spending * region_ratio

    return round(adjusted_spending, 2)

def disposableincome(income, age, state, marital_status):
    return calculate_after_tax_income(income, state, marital_status) - estimate_expenditure(age, state)

def calculate_win_probability(house_edge = 0.0626, profit_factor=0.91):
    p = (1.0 - house_edge) / (1.0 + profit_factor)

    if p < 0.0:
        p = 0.0
    if p > 1.0:
        p = 1.0
    return p



class individual:
    def __init__(self, age, gender, race, income, location, marital_status):
        self.age = age
        self.gender = gender
        self.race = race
        self.income = income
        self.location = location
        self.marital_status = marital_status
        self.risk_tolerance = getTolerance(age, gender, race, income)
        self.income_after_tax = calculate_after_tax_income(income, location, marital_status)
        self.disposable_income = disposableincome(income, age, location, marital_status)
        self.daily_disposable_income = self.disposable_income/365
        self.attributes = self.age, self.gender, self.income, self.location, self.marital_status, self.race

def Simulation(individual):
    daylist = []
    urgelist = []
    winslist = []
    daysgambled = 0
    debtlist = []
    debt = 0
    for i in range(0,365):
        daylist.append(i)
        urge, result = get_gambling_decision(individual.risk_tolerance)
        urgelist.append(urge)
        individual.daily_disposable_income -= sum(debtlist) * 0.0002
        individual.daily_disposable_income = max(0.01, individual.daily_disposable_income)
        if result:
            wager = daily_gambling_spend(individual.daily_disposable_income, individual.risk_tolerance)
            daysgambled += 1
            if wager > (individual.daily_disposable_income): # seeing if individual takes on debt to make wager
                debt = wager - (individual.daily_disposable_income)  # will be negitive bc wager > daily income
            else:
                debt = 0
            if random.random() < calculate_win_probability(house_edge = 0.0626, profit_factor=0.91): #if we win, we add winnings to win list
                    winslist.append(wager*0.91)
                    adjustment = 0.005 * (wager * 0.91 / individual.daily_disposable_income)
                    individual.risk_tolerance = min(1.0, individual.risk_tolerance + adjustment)
            else:
                winslist.append(wager*-1)
                debtlist.append(debt)
        else: #this is for if he didn't gamble
            winslist.append(0)
    return urgelist, winslist, daysgambled, sum(debtlist)


def individualSimulations(person):
    netwin = []
    totaldebt = []
    bankruptcies = 0  # Track bankruptcies
    age, gender, income, location, marital_status, race = person.attributes
    for i in range(0, 1000):
        fresh_person = individual(age, gender, race, income, location, marital_status)
        urgelist, winslist, daysgambled, debt = Simulation(fresh_person)
        netwin.append(sum(winslist))
        totaldebt.append(debt)

        # Check if the person ended the year at the income floor
        if fresh_person.daily_disposable_income <= 0.01:
            bankruptcies += 1

    print(f"net wins: {sum(netwin) / 1000}")
    print(f"debt: {sum(totaldebt) / 1000}")
    print(f"bankruptcy rate: {bankruptcies / 10}%")  # Percentage of 1000
    return sum(netwin) / 1000


Bob = individual(30,"male", "white", 120000, "NY", "single")
Bob_tx = individual(30,"male", "white", 120000, "TX", "single")
Barbra = individual(50, "female", "black", 1000000000000, "MI", "single")
Wesely = individual(18, "male", "asian", 300000, "NY", "single")
Wesely.risk_tolerance = 0.5

individualSimulations(Bob)
individualSimulations(Barbra)
individualSimulations(Wesely)
