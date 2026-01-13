from dataclasses import dataclass
from typing import List
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

