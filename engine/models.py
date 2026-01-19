from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Literal, Any

@dataclass(frozen=True)
class Card:
    rank: str
    colour: Literal["red", "black"]
    value: int

@dataclass
class Company:
    name: str
    cards: List[Card]
    @property
    def liquidation_value(self):
        total = sum(c.value for c in self.cards)
        return max(total, 0)

@dataclass
class Portfolio:
    cash: float
    positions: Dict[str, int] = field(default_factory=dict)

@dataclass
class LogEvent:
    time_step: int
    kind: str
    payload: Dict[str, Any] = field(default_factory=dict)