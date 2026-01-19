from __future__ import annotations
from typing import Dict, List, Tuple
import random

from .models import Card, Company, Portfolio
from .state import GameState

def make_random_card(rng: random.Random) -> Card:
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

def make_company(name: str, rng: random.Random) -> Company:
    cards = [make_random_card(rng) for _ in range(10)]
    return Company(name=name, cards=cards)

def new_game(seed: int | None = None) -> GameState:
    from .state import GameConfig, GameState

    cfg = GameConfig()
    rng = random.Random(seed)

    company_names = ["Red", "Blue", "Green", "Yellow"]
    companies = {name: make_company(name, rng) for name in company_names}

    player = Portfolio(
        cash=cfg.starting_cash,
        positions = {name: cfg.starting_shares for name in company_names}
    )
    index = Portfolio(
        cash=cfg.starting_cash,
        positions = dict(player.positions)
    )
    prices = {name: cfg.starting_price for name in company_names}

    state = GameState(
        companies = companies,
        player = player,
        index = index,
        prices = prices,
        rng = rng,
        config = cfg,
    )
    state.log("START", {"seed":seed, "prices": dict(prices), "positions": dict(player.positions)})
    return state

def compute_liquidation_value(companies: Dict[str, Company], portfolio: Portfolio, interest_rate: float) -> float:
    effective_cash = portfolio.cash
    if effective_cash < 0:
        effective_cash -= interest_rate * abs(effective_cash)

    total = effective_cash
    for name, company in companies.items():
        shares = portfolio.positions.get(name, 0)
        total += shares * company.liquidation_value
    return total

def update_price(current_price: float, rng: random.Random) -> float:
    noise = rng.uniform(-1.0, 1.0)
    new_price = current_price + noise
    return max(new_price, 1)

def generate_sar_report(companies: Dict[str, Company], rng: random.Random) -> Dict[str, int]:
    reports: Dict[str, int] = {}
    for name, company in companies.items():
        sample_cards = rng.sample(company.cards, k=5)
        sar_value = sum(c.value for c in sample_cards)
        reports[name] = sar_value
    return reports

def apply_eps_random_company(companies: Dict[str, Company], rng: random.Random) -> Tuple[str, int, int, int]:
    name = rng.choice(list(companies.keys()))
    company = companies[name]
    old_value = company.liquidation_value
    idx = rng.randrange(len(company.cards))
    company.cards[idx] = make_random_card(rng)
    new_value = company.liquidation_value
    delta = new_value - old_value
    return name, delta, old_value, new_value

def peek_cards(company: Company, rng: random.Random, k: int = 3) -> List[int]:
    sample_cards = rng.choices(company.cards, k=k)
    return [c.value for c in sample_cards]

#----- Actions (Flask routes call) ----#

def trade(state: GameState, company: str, qty: int, side: str) -> None:
    if company not in state.companies:
        raise ValueError("Invalid company")
    if qty <= 0:
        raise ValueError("Invalid qty")
    if side not in ("buy", "sell"):
        raise ValueError("Select buy or sell")

    price = state.prices[company]
    positions = state.player.positions
    cash = state.player.cash
    current_shares = positions.get(company, 0)
    if side == "buy":
        cost = qty * price
        new_cash = cash - cost
        if new_cash < state.config.borrow_limit:
            raise ValueError("Borrow limit reached")
        positions[company] = current_shares + qty
        state.player.cash = new_cash
        state.log("TRADE", {"side": "sell", "company":company, "qty":qty, "price":price, "cash": state.player.cash, "pos": positions[company]})

def peek(state:GameState, company: str) -> List[int]:
    if company not in state.companies:
        raise ValueError("Invalid company")
    if state.player.cash < state.config.peek_cost:
        raise ValueError("Not enough cash for peek")
    state.player.cash -= state.config.peek_cost
    values = peek_cards(state.companies[company], state.rng, k = state.config.peek_k)

def next_step(state: GameState) -> Dict[str, object]:
    state.time_step += 1
    for name in state.prices:
        state.prices[name] = update_price(state.prices[name], state.rng)
    state.log("STEP", {"prices": dict(state.prices)})
    out: Dict[str, object] = {"time_step": state.time_step, "prices": dict(state.prices), "sar": None, "eps": None}
    if state.time_step % state.config.eps_every == 0:
        sar = generate_sar_report(state.companies, state.rng)
        state.log("SAR", {"sar": sar})
        out["sar"] = sar
    if state.time_step % state.config.eps_every == 0:
        company, delta, old_value, new_value = apply_eps_random_company(state.companies, state.rng)
        payload = {"company": company, "delta": delta, "old_value": old_value, "new_value": new_value}
        state.log("EPS", payload)
        out["eps"] = payload
    if state.config.horizon_steps is not None and state.time_step >= state.config.horizon_steps:
        state.log("END_TRIGGER", {"reason": "horizon_reached"})

    return out



