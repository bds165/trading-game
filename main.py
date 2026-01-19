from engine import (
    new_game,
    compute_liquidation_value,
    update_price,
    generate_sar_report,
    apply_eps_random_company,
    peek_cards,
    Portfolio
)
def print_status(companies, portfolio, price: float, time_step: int) -> None:
    print("\n=== CURRENT STATUS ===")
    print(f"Time step: {time_step}")
    print(f"Cash: ${portfolio.cash:.2f}")
    print(f"Market price (all companies): ${price:.2f}")
    print("Positions:")
    for name, shares in portfolio.positions.items():
        print(f"  {name}: {shares} shares")
    print("======================\n")


def main():
    companies, portfolio, price = new_game()
    time_step = 0
    index_portfolio = Portfolio(200.0,
                                positions= dict(portfolio.positions))
    print("Welcome to the Yale Trading Game prototype!")
    print("You start with $200 cash and 5 shares of each company at $40.\n")

    while True:
        print("Actions:")
        print("[e]nd game")
        print("[b]uy shares")
        print("[s]ell shares")
        print("[n]ext step (advance time, update price")
        print("[p]eek at a company's card ($1 cost)")
        choice = input("> ").strip().lower()
        if choice == "e":
            break
        elif choice == "p":
            if portfolio.cash < 1:
                print("You have insufficient cash.")
                continue
            stock = input("Which company's card would you like to peek? Red/Green/Yellow/Blue").strip().title()
            if stock not in companies:
                print("Invalid company.")
                continue
            portfolio.cash -= 1
            values = peek_cards(companies[stock])
            print(f"Peeked {stock}. Sample card values: {values}")
        elif choice == "n":
            price = update_price(price)
            time_step += 1
            print(f"Time step updated to: {time_step}. New price: {price:.2f}")
            if time_step % 3 == 0:
                print(f"\n[SAR] Analyst Reports:")
                sar_reports = generate_sar_report(companies)
                for name, sar in sar_reports.items():
                    print(f"  {name}: {sar}")
            if time_step % 5 == 0:
                print(f"\n[EPS] Earnings Announcement")
                company, delta = apply_eps_random_company(companies)
                sign = "+" if delta >= 0 else ""
                print(f"\n[EPS] announcement for {company}: {sign}{delta:.2f} to fundamental value")

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
                new_cash = portfolio.cash - cost
                if new_cash < -200:
                    print("You cannot borrow that much")
                    continue
                portfolio.cash = new_cash
                current_shares = portfolio.positions.get(stock,0)
                portfolio.positions[stock] = current_shares + qty
                print(f"Bought {qty} shares of {stock} for {cost: .2f}.")
            else:
                new_q = portfolio.positions.get(stock, 0) - qty
                if new_q < -5:
                    print("Cannot short more than 5 shares.")
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
    index_value = compute_liquidation_value(companies, index_portfolio)
    print(f"Market index value: ${index_value:.2f}")
    starting_value = compute_liquidation_value(companies, index_portfolio)
    your_return = (final_value - starting_value) / starting_value * 100
    index_return = (index_value - starting_value) / starting_value * 100
    print(f"Your return is: {your_return:.2f}%")
    print(f"Index return is: {index_return:.2f}%")
    if final_value > index_value:
        print("Congratulations, you beat the index portfolio!")
    else:
        print("Sorry, you underperformed the index portfolio!")






if __name__ == "__main__":
    main()
