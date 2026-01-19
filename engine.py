from dataclasses import dataclass, field
from idlelib.editor import darwin
from typing import List, Dict, Tuple
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

def generate_sar_report(companies: Dict[str, Company]) -> Dict[str, int]:
    reports:Dict[str, int] = {}
    for name, company in companies.items():
        sample_cards = random.sample(company.cards, k=5)
        sar_value = sum(c.value for c in sample_cards) + 50 #(50 is the constant)
        reports[name] = sar_value
    return reports

def apply_eps_random_company (companies: Dict[str, Company]) -> Tuple[str, int]:
    name = random.choice(list(companies.keys()))
    company = companies[name]
    old_value = company.liquidation_value
    idx = random.randrange(len(company.cards))
    company.cards[idx] = make_random_card()
    new_value = company.liquidation_value
    delta = new_value - old_value
    return name, delta

def peek_cards(company: Company, k: int =3) -> List[int]:
    sample_cards = random.choices(company.cards, k=k)
    return [c.value for c in sample_cards]

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
def update_price(current_price: float) -> float:
    noise = random.uniform(-1.0, 1.0)
    new_price = current_price + noise
    if new_price < 1.0:
        new_price = 1.0
    return new_price

