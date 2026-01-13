from engine import make_company, new_game, compute_liquidation_value

def print_status(companies, portfolio, price: float) -> None:
    print("\n=== CURRENT STATUS ===")
    print(f"Cash: ${portfolio.cash:.2f}")
    print(f"Market price (all companies): ${price:.2f}")
    print("Positions:")
    for name, shares in portfolio.positions.items():
        print(f"  {name}: {shares} shares")
    print("======================\n")


def main():
    companies, portfolio, price = new_game()
    print("Welcome to the Yale Trading Game prototype!")
    print("You start with $200 cash and 5 shares of each company at $40.\n")

    while True:
        print("Actions:")
        print("[e]nd game")
        print("[b]uy shares")
        print("[s]ell shares")
        choice = input("> ").strip().lower()
        if choice == "e":
            break
        elif choice == "b" or choice == "s":
            stock = input("Which company? Red/Blue/Green/Yellow: ").strip().title()
            if stock not in companies:
                print("Invalid company.")
                continue
            qty_str = input("How many shares?: ")
            try:
                qty = int(qty_str)
            except ValueError:
                print("Invalid qty.")
                continue
            if qty <= 0:
                print("Invalid qty.")
                continue
            if choice == "b":
                cost = qty * price
                if cost > portfolio.cash:
                    print("Not enough cash.")
                    continue
                portfolio.cash -= cost
                current_shares = portfolio.positions.get(stock,0)
                portfolio.positions[stock] = current_shares + qty
                print(f"Bought {qty} shares of {stock} for {cost: .2f}.")
            else:
                if qty > portfolio.positions.get(stock,0):
                    print("Not enough shares.")
                    continue
                revenue = qty * price
                portfolio.cash += revenue
                current_shares = portfolio.positions.get(stock,0)
                portfolio.positions[stock] = current_shares - qty
                print(f"Sold {qty} shares of {stock} for {revenue: .2f}.")
        else:
            print("Invalid choice.")
    print("GAME OVER")
    print(f"final cash: {portfolio.cash: .2f}")
    for name, company in companies.items():
        print(f"{name} : {company.liquidation_value}")
    final_value = compute_liquidation_value(companies, portfolio)
    print(f"Final value: ${final_value:.2f}")











if __name__ == "__main__":
    main()
