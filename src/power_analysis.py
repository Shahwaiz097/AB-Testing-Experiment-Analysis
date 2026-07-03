from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def required_sample_size(baseline_rate, minimum_detectable_effect, alpha=0.05, power=0.8):
    effect_size = proportion_effectsize(
        baseline_rate,
        baseline_rate + minimum_detectable_effect
    )

    analysis = NormalIndPower()

    required_n = analysis.solve_power(
        effect_size=effect_size,
        power=power,
        alpha=alpha,
        ratio=1
    )

    return required_n