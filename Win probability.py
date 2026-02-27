def calculate_win_probability(house_edge, profit_factor):
    
    p = (1.0 - house_edge) / (1.0 + profit_factor)

    if p < 0.0:
        p = 0.0
    if p > 1.0:
        p = 1.0

    return p

# house_edge = 0.0626
# profit_factor = 0.91