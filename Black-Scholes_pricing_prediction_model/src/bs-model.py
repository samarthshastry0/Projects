# src/bs_model.py
"""
Black-Scholes implementation (European options).
Vectorized-friendly but implemented in plain numpy where helpful.
"""

from dataclasses import dataclass
from typing import Union, Tuple
import numpy as np
from math import log, sqrt, exp
from .utils import norm_cdf, norm_pdf

@dataclass
class BSInput:
    S: float      # Spot price
    K: float      # Strike price
    T: float      # Time to maturity (in years)
    r: float      # Risk-free rate (annual, continuous compounding)
    sigma: float  # Volatility (annual)
    q: float = 0.0  # Dividend yield (annual)

def _d1_d2(S, K, T, r, sigma, q):
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive for d1/d2 calculation.")
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def bs_price(bs: BSInput, option_type: str = "call") -> float:
    """
    Returns Black-Scholes European option price for 'call' or 'put'.
    """
    S, K, T, r, sigma, q = bs.S, bs.K, bs.T, bs.r, bs.sigma, bs.q
    if T == 0:
        # immediate payoff
        if option_type == "call":
            return max(0.0, S - K)
        else:
            return max(0.0, K - S)

    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    # use scalar norm_cdf from utils (works for scalars)
    # if arrays wanted, user can vectorize using numpy functions.
    if option_type == "call":
        price = S * np.exp(-q * T) * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm_cdf(-d2) - S * np.exp(-q * T) * norm_cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return float(price)

def bs_greeks(bs: BSInput, option_type: str = "call") -> dict:
    """
    Returns common Greeks: delta, gamma, vega, theta (per year), rho.
    Theta returned as annualized (i.e., dPrice/dt). Many sources return per-day; adjust if desired.
    """
    S, K, T, r, sigma, q = bs.S, bs.K, bs.T, bs.r, bs.sigma, bs.q
    if T <= 0:
        # For maturity, the Greeks are undefined or degenerate; return zeros or immediate derivatives
        return {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}

    d1, d2 = _d1_d2(S, K, T, r, sigma, q)
    # Use continuous dividend yield q
    pdf_d1 = norm_pdf(d1)
    discount_q = np.exp(-q * T)
    discount_r = np.exp(-r * T)

    gamma = (pdf_d1) / (S * sigma * np.sqrt(T))
    vega = S * discount_q * pdf_d1 * np.sqrt(T)  # per 1 vol (i.e., if sigma in decimals)
    if option_type == "call":
        delta = discount_q * norm_cdf(d1)
        theta = (-S * pdf_d1 * sigma * discount_q) / (2 * np.sqrt(T)) - r * K * discount_r * norm_cdf(d2) + q * S * discount_q * norm_cdf(d1)
        rho = K * T * discount_r * norm_cdf(d2)
    else:
        delta = discount_q * (norm_cdf(d1) - 1)
        theta = (-S * pdf_d1 * sigma * discount_q) / (2 * np.sqrt(T)) + r * K * discount_r * norm_cdf(-d2) - q * S * discount_q * norm_cdf(-d1)
        rho = -K * T * discount_r * norm_cdf(-d2)

    # Return theta as per-year; divide by 365 if you want per-day
    return {
        "delta": float(delta),
        "gamma": float(gamma),
        "vega": float(vega),
        "theta": float(theta),
        "rho": float(rho)
    }

def implied_volatility(target_price: float, bs: BSInput, option_type: str = "call", tol=1e-6, max_iter=100) -> float:
    """
    Simple Newton-Raphson to solve for implied volatility.
    Starts from initial guess sigma=0.2. Falls back to bisection if NR fails.
    """
    S, K, T, r, q = bs.S, bs.K, bs.T, bs.r, bs.q
    if target_price <= 0:
        return 0.0

    sigma = 0.2
    for i in range(max_iter):
        bs_try = BSInput(S=S, K=K, T=T, r=r, sigma=sigma, q=q)
        price = bs_price(bs_try, option_type)
        vega = bs_greeks(bs_try, option_type)["vega"]
        diff = price - target_price
        if abs(diff) < tol:
            return sigma
        # safeguard for zero vega
        if vega < 1e-8:
            break
        sigma = sigma - diff / vega
        if sigma <= 0 or sigma > 5:
            break

    # fallback: bisection between near-zero and large vol
    low, high = 1e-8, 5.0
    for _ in range(100):
        mid = 0.5 * (low + high)
        price_mid = bs_price(BSInput(S=S, K=K, T=T, r=r, sigma=mid, q=q), option_type)
        if abs(price_mid - target_price) < tol:
            return mid
        if price_mid > target_price:
            high = mid
        else:
            low = mid
    return mid
