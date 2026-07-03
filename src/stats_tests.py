import numpy as np
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

def two_proportion_test(test_successes, test_n, control_successes, control_n):
    count = np.array([test_successes, control_successes])
    nobs = np.array([test_n, control_n])

    z_stat, p_value = proportions_ztest(count, nobs)

    ci_low, ci_high = confint_proportions_2indep(
        count1=test_successes,
        nobs1=test_n,
        count2=control_successes,
        nobs2=control_n,
        method="wald"
    )

    return {
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high
    }
    