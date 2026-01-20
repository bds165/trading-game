from __future__ import annotations

from flask import Blueprint, render_template, request, redirect, url_for, flash
from engine import new_game, trade, peek, next_step

bp = Blueprint("game", __name__)

#---- Single Player in Memory ----#

STATE = new_game(seed = None)
def _last_events(n: int = 20):
    return STATE.logs[-n:]

@bp.get("/")
def index():
    return render_template(
        "game/index.html",
        state = STATE,
        events = _last_events(20),
    )
@bp.post("/new")
def new():
    global STATE
    seed_raw = request.form.get("seed","").strip()
    seed = None
    if seed_raw:
        try:
            seed = int(seed_raw)
        except ValueError:
            flash("Need seed to be an integer or left blank.", "error")
            return redirect(url_for("game.index"))
    STATE = new_game(seed = seed)
    flash("New game started.", "ok")
    return redirect(url_for("game.index"))

@bp.post("/trade")
def do_trade():
    company = request.form.get("company", "").strip().title()
    side = request.form.get("side", "").strip().lower()
    qty_raw = request.form.get("qty", "").strip()

    try:
        qty = int(qty_raw)
    except ValueError:
        flash("Quantity needs to be an integer.", "error")
        return redirect(url_for("game.index"))
    try:
        trade(STATE, company, qty, side)
        flash(f"{side.title()} {qty} of {company} has been traded.", "ok")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("game.index"))

@bp.post("/peek")
def do_peek():
    company = request.form.get("company", "").strip().title()
    try:
        values = peek(STATE, company)
        flash(f"Peeked {company.title()}: {values}", "ok")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("game.index"))

@bp.post("/next")
def do_next():
    out = next_step(STATE)
    msg = f"Advanced to step {out['time_step']}."
    if out.get("sar") is not None:
        msg += " SAR released."
    if out.get("eps") is not None:
        eps = out["eps"]
        msg += f" EPS: {eps['company']} ({eps['delta']:+})."
    flash(msg, "ok")
    return redirect(url_for("game.index"))

