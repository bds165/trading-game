from dataclasses import dataclass, field
from idlelib.editor import darwin
from typing import List, Dict
import random

@dataclass
class Card:
    rank: str
    colour: str
    value: int

@dataclass
class Company:
    name: str
    cards: List[Card]

    @property
    def liquidation_value(self) -> int:
        total = sum(c.value for c in self.cards)
        return max(total,0)

def make_random_card() -> Card:
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    rank = random.choice(ranks)
    if rank in ["J", "Q", "K"]:
        base = 10
    elif rank == "A":
        base = 20
    else:
        base = int(rank)
    colour = random.choice(["red", "black"])
    if colour == "black":
        value = base *2
    else:
        value = -base
    return Card(rank=rank, colour=colour, value=value)

def make_company(name: str) -> Company:
    cards = [make_random_card() for _ in range(10)]
    return Company(name=name, cards=cards)
@dataclass
class Portfolio:
    cash: float = 200.0
    positions: Dict[str, int] = field(default_factory=dict)

def new_game():
    company_names = ["Red", "Blue", "Green", "Yellow"]
    companies = {
        name: make_company(name)
        for name in company_names
    }
    portfolio = Portfolio(
        cash = 200.0,
        positions = {name: 5 for name in company_names}
    )
    price_per_share = 40.0
    return companies, portfolio, price_per_share
def compute_liquidation_value(companies: Dict[str, Company], portfolio: Portfolio)->float:
    effective_cash = portfolio.cash
    if effective_cash < 0:
        interest = 0.10 * abs(effective_cash)
        effective_cash -= interest
    total = effective_cash
    for name, company in companies.items():
        shares = portfolio.positions.get(name, 0)
        lv_per_share = company.liquidation_value
        total += shares * lv_per_share
    return total


