import pytest
from engine import new_game, trade, peek, next_step

def test_determinism_same_seed_start():
    s1 = new_game(1)
    s2 = new_game(1)
    assert s1.prices == s2.prices
    lv1 = {name: c.liquidation_value for name, c in s1.companies.items()}
    lv2 = {name: c.liquidation_value for name, c in s2.companies.items()}
    assert lv1 == lv2

def test_borrow_limit():
    s1 = new_game(123)
    with pytest.raises(ValueError):
        trade(s1, "Red", 11, "sell")
def test_short_limit():
    s1 = new_game(123)
    with pytest.raises(ValueError):
        trade(s1, "Red", 11, "sell")

def test_logs_update_position_cash():
    s1 = new_game(123)
    before_cash = s1.player.cash
    before_pos = s1.player.positions["Red"]
    price = s1.prices["Red"]
    trade(s1, "Red", 2, "buy")
    assert s1.player.positions["Red"] == before_pos + 2
    assert s1.player.cash == before_cash - price * 2

    last_log = s1.logs[-1]
    assert last_log.kind == "TRADE"
    assert last_log.payload["side"] == "buy"
    assert last_log.payload["qty"] == 2
    assert last_log.payload["company"] == "Red"

def test_peek_returns_values_deducts_cash_logs():
    s1 = new_game(123)
    before_cash = s1.player.cash
    values = peek(s1, "Red")
    assert isinstance(values, list)
    assert len(values) == s1.config.peek_k
    assert s1.player.cash == before_cash - s1.config.peek_cost
    last_log = s1.logs[-1]
    assert last_log.kind == "PEEK"
    assert last_log.payload["company"] == "Red"
    assert last_log.payload["values"] == values

def test_next_step_triggers_sar_eps():
    s1 = new_game(123)
    out = None
    for _ in range(3):
        out = next_step(s1)
    assert out is not None
    assert out["eps"] is None
    assert out["sar"] is not None
    for _ in range(5):
        out = next_step(s1)
    assert out is not None
    assert out["sar"] is None