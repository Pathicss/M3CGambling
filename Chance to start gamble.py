def get_age_bracket(age):
    if age < 18:
        return None
    elif 18 <= age <= 24:
        return "18-24"
    elif 25 <= age <= 34:
        return "25-34"
    elif 35 <= age <= 44:
        return "35-44"
    elif 45 <= age <= 54:
        return "45-54"
    elif 55 <= age <= 64:
        return "55-64"
    else:
        return "65+"

def get_income_bracket(income):
    if income < 55820:
        return "lower"
    elif 55820 <= income <= 167460:
        return "middle"
    else:
        return "higher"

age_likelihood = {
    "18-24": 17,
    "25-34": 26,
    "35-44": 21,
    "45-54": 13,
    "55-64": 16,
    "65+": 8
}

ethnicity_likelihood = {
    "white": 19,
    "black": 30,
    "hispanic": 27,
    "asian": 22
}

gender_likelihood = {
    "male": 68,
    "female": 32
}

income_likelihood = {
    "lower": 21,
    "middle": 23,
    "higher": 26
}

age = int(input("Enter age: "))
eth = input("Enter ethnicity (white, black, hispanic, asian): ").strip().lower()
gender = input("Enter gender (male, female): ").strip().lower()
income = float(input("Enter household income: "))

bracket = get_age_bracket(age)
if bracket is None:
    print("Under 18: Gambling participation is restricted.")
    exit()

if eth not in ethnicity_likelihood:
    print("Ethnicity not recognized. Choose from white, black, hispanic, asian.")
    exit()

if gender not in gender_likelihood:
    print("Gender not recognized. Choose male or female.")
    exit()

income_bracket = get_income_bracket(income)

age_percent = age_likelihood[bracket]
eth_percent = ethnicity_likelihood[eth]
gender_percent = gender_likelihood[gender]
income_percent = income_likelihood[income_bracket]

combined = (age_percent + eth_percent + gender_percent + income_percent) / 4

print("\nResults:")
print(f"Age bracket: {bracket} → {age_percent}% likelihood")
print(f"Ethnicity: {eth} → {eth_percent}% likelihood")
print(f"Gender: {gender} → {gender_percent}% likelihood")
print(f"Income bracket: {income_bracket} → {income_percent}% likelihood")

print(f"\nCombined estimated likelihood: {combined:.2f}%")


