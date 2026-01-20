from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random

from .models import Company, Portfolio, LogEvent

@dataclass
class GameConfig:
    starting_cash: float = 200.0
    starting_shares: int = 5
    starting_price: float = 40.0

    borrow_limit: float = -200.0
    short_limit: int = -5
    interest_rate: float = 0.10

    peek_cost: float = 1.0
    peek_k: int = 3
    sar_every: int = 3
    eps_every: int = 5

    horizon_steps: Optional[int] = None

@dataclass
class GameState:
    companies: Dict[str, Company]
    player: Portfolio
    index: Portfolio
    prices: Dict[str, float]
    time_step: int = 0
    logs: List[LogEvent] = field(default_factory=list)
    rng: random.Random = field(default=random.Random)
    config: GameConfig = field(default_factory=GameConfig)

    def log(self, kind: str, payload: dict) -> None:
        self.logs.append(LogEvent(time_step = self.time_step, kind = kind, payload = payload))