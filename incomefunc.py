ageIn = {
    "Under 25": 48514,
    "25-34": 102494,
    "35-44": 128285,
    "45-54": 100327,
    "55-64": 121571,
    "65-74": 75460,
    "75+": 56028
}
regionIn = {
    "Northeast": 115770,
    "Midwest": 97104,
    "South": 93814,
    "West": 120365
}

regionInAvg = sum(regionIn.values())/4

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

def estimate_income(age, state):
    state = state.upper()

    if state not in state_to_region:
        raise ValueError("Invalid state abbreviation.")

    region = state_to_region[state]
    age_group = get_age_group(age)

    base_spending = ageIn[age_group]
    region_ratio = regionIn[region] / regionInAvg
    adjusted_spending = base_spending * region_ratio

    return round(adjusted_spending, 2)

print(estimate_income(65, "CA"))