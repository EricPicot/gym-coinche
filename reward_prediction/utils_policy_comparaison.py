import numpy as np
import pandas as pd
import scipy.stats as scs


def size_sample_AB_test(risk1, risk2, var, mde, bilateral=False):
    if bilateral:
        Z_alpha = scs.norm(0, 1).ppf(1 - risk1 / 2)
    else:
        Z_alpha = scs.norm(0, 1).ppf(1 - risk1)

    Z_beta = scs.norm(0, 1).ppf(1 - risk2)

    min_N = (2 * (var) * (Z_beta + Z_alpha) ** 2 / mde ** 2)

    return min_N


def test_H0(x_A, x_B, risk1, bilateral=False):
    # Calcul de t_AB : différence des moyennes normalisée
    diff_mean = (np.mean(x_B) - np.mean(x_A))  # diff entre les moyennes

    # Estimation de l'écart-type joint
    std_pooled = np.sqrt((np.var(x_B) / len(x_B)) + (np.var(x_A) / len(x_A)))
    stat = diff_mean / std_pooled  # différence normalisée

    # Seuil correspondant au risk de première espèce défini
    if bilateral:
        t = scs.norm(0, 1).ppf(1 - risk1 / 2)
        return np.abs(stat < t), t, stat
    else:
        t = scs.norm(0, 1).ppf(1 - risk1)
        return (stat < t), t, stat


def power_test(x_A, x_B, mde, risk1, bilateral=False):
    var_A = np.var(x_A)
    var_B = np.var(x_B)
    N_A = len(x_A)
    N_B = len(x_B)

    std_pooled = np.sqrt(var_A / N_A + var_B / N_B)
    expectation = mde / std_pooled
    t = test_H0(x_A, x_B, risk1, bilateral)[1]

    return (1 - scs.norm(expectation, 1).cdf(t))

def confidence_interval_diff(x_A, x_B, sig_level=0.05):

    mean_diff = np.mean(x_B) - np.mean(x_A)
    var_diff = np.var(x_B)/len(x_B) + np.var(x_A)/len(x_A)

    gap = (scs.norm(0, 1).ppf(1 - sig_level/2))*np.sqrt(var_diff)

    min_ = mean_diff - gap
    max_ = mean_diff + gap

    return min_, max_, scs.norm(0, 1).ppf(1 - sig_level/2)