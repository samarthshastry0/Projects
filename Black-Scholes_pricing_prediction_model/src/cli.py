# src/cli.py
"""
Simple command-line interface to price an option.
Run: python -m src.cli --help
"""
import argparse
from .bs_model import BSInput, bs_price, bs_greeks, implied_volatility

def main():
    parser = argparse.ArgumentParser(description="Black-Scholes pricer")
    parser.add_argument("--S", type=float, required=True, help="Spot price")
    parser.add_argument("--K", type=float, required=True, help="Strike price")
    parser.add_argument("--T", type=float, required=True, help="Time to maturity (years)")
    parser.add_argument("--r", type=float, default=0.01, help="Risk-free rate (annual, decimal)")
    parser.add_argument("--sigma", type=float, default=0.2, help="Volatility (annual, decimal)")
    parser.add_argument("--q", type=float, default=0.0, help="Dividend yield (annual, decimal)")
    parser.add_argument("--type", choices=["call","put"], default="call")
    parser.add_argument("--iv", action="store_true", help="Compute implied vol for given market price (use --market_price)")
    parser.add_argument("--market_price", type=float, help="Market price for IV calculation")

    args = parser.parse_args()
    bs = BSInput(S=args.S, K=args.K, T=args.T, r=args.r, sigma=args.sigma, q=args.q)
    price = bs_price(bs, args.type)
    greeks = bs_greeks(bs, args.type)
    print(f"{args.type.title()} price: {price:.6f}")
    print("Greeks:")
    for k,v in greeks.items():
        print(f"  {k}: {v:.6f}")

    if args.iv:
        if args.market_price is None:
            print("Provide --market_price to compute implied volatility.")
        else:
            iv = implied_volatility(args.market_price, bs, args.type)
            print(f"Implied volatility: {iv:.6%}")

if __name__ == "__main__":
    main()
