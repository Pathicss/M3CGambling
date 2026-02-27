import numpy as np
from scipy.stats import beta


def get_gambling_decision(tolerance):
    """
    tolerance: 0.0 to 1.0
    Returns: (float) daily_urge, (bool) did_gamble
    """
    # 1. Map Affinity to Target Mode (The 'Peak' probability)
    # 0.5->25%, 0.75->50%, 0.8->75%, 1.0->100%
    xp = [0, 0.5, 0.75, 0.8, 1.0]
    fp = [0, 0.25, 0.5, 0.75, 1.0]
    target_mode = np.interp(tolerance, xp, fp)

    # 2. Fixed Concentration (Kappa)
    # A value of 50 makes a clear unimodal peak for all gamblers.
    kappa = 50

    # 3. Derive Alpha (a) and Beta (b)
    # Keeping m between 0.001 and 0.999 ensures the math doesn't break.
    m = np.clip(target_mode, 0.001, 0.999)
    a = m * (kappa - 2) + 1
    b = (1 - m) * (kappa - 2) + 1

    # 4. Sample the Urge (Randomly pick from the distribution)
    daily_urge = np.random.beta(a, b)

    # 5. Final Decision (Roll the dice)
    did_gamble = np.random.random() < daily_urge

    return daily_urge, did_gamble
