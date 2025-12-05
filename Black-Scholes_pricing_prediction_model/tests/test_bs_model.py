# tests/test_bs_model.py
import math
from src.bs_model import BSInput, bs_price, bs_greeks, implied_volatility

def almost_equal(a, b, tol=1e-6):
    return abs(a-b) < tol

def test_bs_price_call_vs_put_parity():
    bs = BSInput(S=100, K=100, T=0.5, r=0.01, sigma=0.2, q=0.0)
    c = bs_price(bs, "call")
    p = bs_price(bs, "put")
    # put-call parity: C - P = S*e^{-qT} - K*e^{-rT}
    lhs = c - p
    rhs = bs.S * math.exp(-bs.q*bs.T) - bs.K * math.exp(-bs.r*bs.T)
    assert almost_equal(lhs, rhs, tol=1e-6)

def test_greeks_reasonable():
    bs = BSInput(S=120, K=100, T=0.25, r=0.02, sigma=0.35, q=0.0)
    greeks = bs_greeks(bs, "call")
    # delta between 0 and 1, gamma positive, vega positive
    assert 0.0 <= greeks["delta"] <= 1.0
    assert greeks["gamma"] > 0
    assert greeks["vega"] > 0

def test_implied_vol_recovery():
    bs = BSInput(S=150, K=100, T=1.0, r=0.01, sigma=0.3, q=0.0)
    true_price = bs_price(bs, "call")
    guessed_iv = implied_volatility(true_price, BSInput(S=bs.S,K=bs.K,T=bs.T,r=bs.r,sigma=0.2,q=bs.q), "call")
    assert abs(guessed_iv - bs.sigma) < 1e-3
