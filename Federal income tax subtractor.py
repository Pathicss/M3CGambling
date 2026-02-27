def tax_owed(x):
    if x <= 11600:
        return 0.10 * x
    elif x <= 47150:
        return 1160 + 0.12 * (x - 11600)
    elif x <= 100525:
        return 5426 + 0.22 * (x - 47150)
    elif x <= 191950:
        return 17168.50 + 0.24 * (x - 100525)
    elif x <= 243725:
        return 39110.50 + 0.32 * (x - 191950)
    elif x <= 609350:
        return 55678.50 + 0.35 * (x - 243725)
    else:
        return 191253.25 + 0.37 * (x - 609350)

income = float(input("income:"))

tax = tax_owed(income)
effective_rate = (tax / income) * 100 if income > 0 else 0

print(f"Tax owed: ${tax:,.2f}")