import random

# -----------------------------
# AGE DATA
# -----------------------------
age_data = {
    "18-24": {"Non-PG": (92,192), "Low": (34,192), "Moderate": (28,192), "High": (38,192)},
    "25-34": {"Non-PG": (237,427), "Low": (65,427), "Moderate": (52,427), "High": (73,427)},
    "35-44": {"Non-PG": (312,466), "Low": (49,466), "Moderate": (50,466), "High": (55,466)},
    "45-54": {"Non-PG": (332,451), "Low": (66,451), "Moderate": (32,451), "High": (21,451)},
    "55-64": {"Non-PG": (243,292), "Low": (30,292), "Moderate": (12,292), "High": (7,292)},
    "65+":   {"Non-PG": (295,345), "Low": (33,345), "Moderate": (15,345), "High": (2,345)}
}

# -----------------------------
# GENDER DATA
# -----------------------------
gender_data = {
    "male":   {"Non-PG": (695,1101), "Low": (150,1101), "Moderate": (120,1101), "High": (136,1101)},
    "female": {"Non-PG": (815,1072), "Low": (127,1072), "Moderate": (70,1072),  "High": (60,1072)}
}

# -----------------------------
# RACE / ETHNICITY DATA
# -----------------------------
race_data = {
    "white":   {"Non-PG": (1016,1341), "Low": (155,1341), "Moderate": (90,1341), "High": (80,1341)},
    "hispanic":{"Non-PG": (245,394),   "Low": (40,394),   "Moderate": (49,394), "High": (60,394)},
    "black":   {"Non-PG": (155,261),   "Low": (51,261),   "Moderate": (27,261), "High": (28,261)},
    "asian":   {"Non-PG": (94,177),    "Low": (31,177),   "Moderate": (24,177), "High": (28,177)}
}

# -----------------------------
# INCOME DATA
# -----------------------------
income_data = {
    "<15k":        {"Non-PG": (65,101),  "Low": (14,101), "Moderate": (9,101),  "High": (13,101)},
    "15-29k":      {"Non-PG": (137,204), "Low": (19,204), "Moderate": (30,204), "High": (18,204)},
    "30-49k":      {"Non-PG": (207,309), "Low": (53,309), "Moderate": (28,309), "High": (21,309)},
    "50-69k":      {"Non-PG": (256,396), "Low": (54,396), "Moderate": (42,396), "High": (44,396)},
    "70-99k":      {"Non-PG": (305,439), "Low": (57,439), "Moderate": (36,439), "High": (41,439)},
    "100-124k":    {"Non-PG": (198,286), "Low": (36,286), "Moderate": (18,286), "High": (34,286)},
    "125-149k":    {"Non-PG": (120,159), "Low": (15,159), "Moderate": (10,159), "High": (14,159)},
    "150k+":       {"Non-PG": (222,279), "Low": (29,279), "Moderate": (17,279), "High": (11,279)}
}

# -----------------------------
# HELPERS
# -----------------------------
def get_age_bracket(age):
    if 18 <= age <= 24: return "18-24"
    if 25 <= age <= 34: return "25-34"
    if 35 <= age <= 44: return "35-44"
    if 45 <= age <= 54: return "45-54"
    if 55 <= age <= 64: return "55-64"
    if age >= 65: return "65+"
    return None

def get_income_bracket(income):
    if income < 15000: return "<15k"
    if income < 30000: return "15-29k"
    if income < 50000: return "30-49k"
    if income < 70000: return "50-69k"
    if income < 100000: return "70-99k"
    if income < 125000: return "100-124k"
    if income < 150000: return "125-149k"
    return "150k+"

def convert_to_probabilities(raw):
    return {cat: num/den for cat, (num,den) in raw.items()}

def average_four(a, b, c, d):
    return {cat: (a[cat] + b[cat] + c[cat] + d[cat]) / 4 for cat in a}

def assign_category(probabilities):
    cats = list(probabilities.keys())
    probs = list(probabilities.values())
    return random.choices(cats, weights=probs, k=1)[0]

def assign_tolerance(category):
    if category == "Non-PG": return random.uniform(0, 0.25)
    if category == "Low": return random.uniform(0.25, 0.50)
    if category == "Moderate": return random.uniform(0.50, 0.75)
    if category == "High": return random.uniform(0.75, 1.00)

# -----------------------------
# USER INPUT
# -----------------------------


# -----------------------------
# PROCESSING
# -----------------------------
def getTolerance(age, gender, race, income_value):
    age_bracket = get_age_bracket(age)
    income_bracket = get_income_bracket(income_value)

    age_probs = convert_to_probabilities(age_data[age_bracket])
    gender_probs = convert_to_probabilities(gender_data[gender])
    race_probs = convert_to_probabilities(race_data[race])
    income_probs = convert_to_probabilities(income_data[income_bracket])

    combined = average_four(age_probs, gender_probs, race_probs, income_probs)
    assigned = assign_category(combined)
    tolerance = assign_tolerance(assigned)
    return tolerance
