# notebooks/example.py
from src.bs_model import BSInput, bs_price, bs_greeks, implied_volatility
import matplotlib.pyplot as plt
import numpy as np

# example
bs = BSInput(S=100, K=100, T=30/365, r=0.02, sigma=0.25, q=0.0)
print("Call price:", bs_price(bs,"call"))
print("Greeks:", bs_greeks(bs,"call"))

# Plot call price vs strike
strikes = np.linspace(60,140,81)
prices = [bs_price(BSInput(S=100,K=K,T=bs.T,r=bs.r,sigma=bs.sigma,q=bs.q),"call") for K in strikes]
plt.plot(strikes, prices)
plt.xlabel("Strike")
plt.ylabel("Call price")
plt.title("Call price vs Strike")
plt.show()
