import plotly.graph_objects as go
from main import *
import random


def plot_person_simulation(person_instance):
    """
    Plots a 365-day simulation of a person's daily disposable income.
    Includes Initial Tolerance and Initial Annual Income in the labels and title.
    """
    # 1. Capture initial values for labeling
    init_tolerance = round(person_instance.risk_tolerance, 3)
    init_annual_income = person_instance.income

    days = list(range(1, 366))
    income_history = []
    debt_list = []

    # Track current state for simulation
    current_daily_income = person_instance.daily_disposable_income
    current_risk_tolerance = person_instance.risk_tolerance

    for day in days:
        # Apply debt interest penalty (0.01% of accumulated debt)
        interest_penalty = sum(debt_list) * 0.0001
        current_daily_income = max(0.01, current_daily_income - interest_penalty)

        # Decide whether to gamble today
        urge, did_gamble = get_gambling_decision(current_risk_tolerance)

        if did_gamble:
            wager = daily_gambling_spend(current_daily_income, current_risk_tolerance)

            # House Edge Calculation (6.26% edge, 0.91 profit factor)
            win_prob = (1.0 - 0.0626) / (1.0 + 0.91)

            if random.random() < win_prob:
                # WIN: Income increases, and risk tolerance climbs
                winnings = wager * 0.91
                current_daily_income += winnings
                adjustment = 0.005 * (winnings / max(0.01, current_daily_income))
                current_risk_tolerance = min(1.0, current_risk_tolerance + adjustment)
            else:
                # LOSS: Income decreases; remaining wager balance becomes debt
                if wager > current_daily_income:
                    debt_amount = wager - current_daily_income
                    debt_list.append(debt_amount)
                    current_daily_income = 0.01
                else:
                    current_daily_income -= wager

        income_history.append(current_daily_income)

    # 2. Create Plotly Figure
    fig = go.Figure()

    # Legend label including specific initial stats
    trace_label = f"Daily Income (Start Tol: {init_tolerance}, Income: ${init_annual_income:,})"

    fig.add_trace(go.Scatter(
        x=days,
        y=income_history,
        mode='lines',
        name=trace_label,
        line=dict(color='#636EFA', width=2)
    ))

    # Updated layout with subtitle and detailed axis labels
    fig.update_layout(
        title={
            'text': (f"365-Day Simulation for Person in {person_instance.location}<br>"
                     f"<sup>Initial Annual Income: ${init_annual_income:,} | "
                     f"Initial Risk Tolerance: {init_tolerance}</sup>"),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Day of Year",
        yaxis_title="Disposable Income ($)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(t=100)  # Space for the larger title
    )

    return fig

plot_person_simulation(Wesely).show()