from engine import make_company


def main():
    company = make_company("Blue")
    print("Company:", company.name)
    print("Cards:")
    for c in company.cards:
        print(f"  {c.colour} {c.rank} -> {c.value}")
    print("\nLiquidation value:", company.liquidation_value)


if __name__ == "__main__":
    main()
