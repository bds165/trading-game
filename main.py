from engine import make_company, new_game, compute_liquidation_value


def main():
    companies, portfolio, price = new_game()
    print("=== New Game ===")
    print(f"Starting cash: ${portfolio.cash:.2f}")
    print(f"Initial market price (all companies): {price:.2f}")
    print(f"Starting positions:")
    for name, shares in portfolio.positions.items():
        print(f"{name}: {shares} shares")
    print("\n[Debug] Hidden Liquidation Values per Share:")
    for name, company in companies.items():
        print(f"{name} : {company.liquidation_value}")
    final_value = compute_liquidation_value(companies, portfolio)
    print(f"Final value: ${final_value:.2f}")


if __name__ == "__main__":
    main()
