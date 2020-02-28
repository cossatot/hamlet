"""
This module provides statistical functions that are not specific to any set of
tests.
"""

from typing import Optional

import numpy as np
from scipy.special import gamma, factorial
from scipy.optimize import minimize


def sample_event_times_in_interval(
        annual_occurrence_rate: float,
        interval_length: float,
        t0: float = 0.,
        rand_seed: Optional[int] = None) -> np.ndarray:
    """
    Returns the times of events 

    """

    if rand_seed is not None:
        np.random.seed(rand_seed)

    n_events = np.random.poisson(annual_occurrence_rate * interval_length)

    event_times = np.random.uniform(low=t0,
                                    high=t0 + interval_length,
                                    size=n_events)
    return event_times


def poisson_likelihood(num_events: int,
                       rate: float,
                       time_interval: float = 1.,
                       not_modeled_val: float = 0.) -> float:
    """
    Returns the Poisson likelihood of observing `num_events` in a
    `time_interval` given the `rate` of those events in the units of the time
    interval (i.e., if the `time_interval` is in years, the rate is the annual
    occurrence rate).

    If `rate` > 0, the Poisson likelihood is defined as

    :math:`L(n|rt) = (rt)^n \\exp(-rt) / n!`

    where `n` is `num_events`, `r` is `rate`, `t` is `time_interval`, and
    `L(n|rt)` is the Poisson likeihood.

    If `rate` = 0, then the `not_modeled_val` is returned.
    """
    if rate == 0:
        return poisson_likelihood_zero_rate(num_events, not_modeled_val)
    else:
        rt = rate * time_interval
        return np.exp(-rt) * rt**num_events / np.math.factorial(num_events)


def poisson_likelihood_zero_rate(num_events: int,
                                 not_modeled_val: float = 0.) -> float:
    if num_events == 0:
        return 1.
    elif num_events > 0:
        return not_modeled_val
    else:
        raise ValueError("num_events should be zero or a positive integer.")


def poisson_log_likelihood(num_events: int,
                           rate: float,
                           time_interval: float = 1.,
                           not_modeled_val: float = 0.) -> float:
    if rate == 0.:
        return np.log(poisson_likelihood_zero_rate(rate, not_modeled_val))
    else:
        rt = rate * time_interval
        return (-1 * rt + num_events * np.log(rt) -
                np.log(np.math.factorial(rt)))


def negative_binomial_distribution(num_events: int, mean_rate: float,
                                   dispersion: float) -> float:
    """
    Returns the negative binomial probability for observing 

    """
    if dispersion == 0.:
        return poisson_likelihood(num_events, mean_rate)

    r_disp = 1 / dispersion

    term_1 = (gamma(num_events + r_disp)) / (gamma(r_disp) *
                                             factorial(num_events))
    term_2 = ((mean_rate * dispersion) /
              (1 + mean_rate * dispersion))**num_events
    term_3 = (1 + mean_rate * dispersion)**r_disp

    return term_1 * term_2 * term_3


def estimate_negative_binom_parameters(samples):

    mean = np.mean(samples)
    cov = np.std(samples) / mean

    print(cov)

    def neg_neg_binom_likelihood(dispersion):
        neg_like = -1 * np.sum([
            np.log(negative_binomial_distribution(n, mean, dispersion))
            for n in samples
        ])
        return neg_like

    dispersion = minimize(neg_neg_binom_likelihood, cov, method='BFGS').x[0]

    return (mean, dispersion)


def kullback_leibler_divergence(p, q):
    """
    The Kullback-Leibler Divergence is a measure of the information loss in
    moving from a distribution P to a second distribution Q that may be a model
    or approximation.
    """

    # TODO: deal w/ zero probabilities

    pp = np.asarray(p)
    qq = np.asarray(q)

    return np.sum(pp * np.log(pp / qq))


def jensen_shannon_divergence(p, q):

    pp = np.asarray(p)
    qq = np.asarray(q)

    r = _mid_pt_measure(pp, qq)

    return 0.5 * (kullback_leibler_divergence(pp, r) +
                  kullback_leibler_divergence(qq, r))


def jensen_shannon_distance(p, q):
    return np.sqrt(jensen_shannon_divergence(p, q))


def _mid_pt_measure(p, q):
    return 0.5 * (p + q)
