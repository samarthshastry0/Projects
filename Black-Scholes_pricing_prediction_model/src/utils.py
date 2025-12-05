import math

def norm_cdf(x):
    """
    Standard normal CDF using math.erf for portability (no scipy required).
    """
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)