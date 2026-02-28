import plotly.graph_objects as go
import random
from main import *

def plot_person_simulation(person_instance):
    """
    Plots a 365-day simulation of a person's daily disposable income.
    - No markers or arrows.
    - No debt line.
    - Includes Gender in the title and legend.
    """
    # 1. Capture metadata for labeling
    init_tol = round(person_instance.risk_tolerance, 3)
    init_annual_inc = person_instance.income
    age = person_instance.age
    gender = person_instance.gender.capitalize()
    loc = person_instance.location

    days = list(range(1, 366))
    income_history = []
    debt_list = []

    current_inc = person_instance.daily_disposable_income
    current_tol = person_instance.risk_tolerance

    # 2. Run Simulation
    for day in days:
        # Apply debt interest penalty (internal logic remains)
        current_inc = max(0.01, current_inc - sum(debt_list) * 0.0001)

        urge, did_gamble = get_gambling_decision(current_tol)

        if did_gamble:
            wager = daily_gambling_spend(current_inc, current_tol)
            win_prob = (1.0 - 0.0626) / (1.0 + 0.91)

            if random.random() < win_prob:
                result = wager * 0.91
                current_inc += result
                current_tol = min(1.0, current_tol + 0.005 * (result / max(0.01, current_inc)))
            else:
                current_inc -= wager
                if current_inc < 0:
                    debt_list.append(abs(current_inc))
                    current_inc = 0.01

        income_history.append(current_inc)

    # 3. Create Figure
    fig = go.Figure()

    # Main Income Trace only
    fig.add_trace(go.Scatter(
        x=days, y=income_history, mode='lines',
        name=f"Disposable Income ({gender})",
        line=dict(color='#636EFA', width=2)
    ))

    fig.update_layout(
        title={
            'text': (f"365-Day Simulation for {age}yr old {gender} in {loc}<br>"
                     f"<sup>Initial Annual Income: ${init_annual_inc:,} | "
                     f"Initial Risk Tolerance: {init_tol}</sup>"),
            'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title="Day of Year",
        yaxis_title="Disposable Income ($)",
        template="plotly_white",
        hovermode="x unified"
    )

    return fig

plot_person_simulation(Wesely).show() #input a person object here