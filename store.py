from telethon.tl import functions
from util import safe_int, gift_label_from_star_gift

async def fetch_store_gifts(client):
    return await client(functions.payments.GetStarGiftsRequest(hash=0))

def format_store_gift(g):
    gid = getattr(g, "id", None)
    stars = safe_int(getattr(g, "stars", 0))
    sold_out = bool(getattr(g, "sold_out", False))
    limited = bool(getattr(g, "limited", False))
    require_premium = bool(getattr(g, "require_premium", False))

    label = gift_label_from_star_gift(g)
    flags = []
    if sold_out: flags.append("SOLD_OUT")
    if limited: flags.append("LIMITED")
    if require_premium: flags.append("PREMIUM")

    return f"gift_id={gid} | {stars}⭐ | {label}" + (f" | {' '.join(flags)}" if flags else "")

async def list_store_gifts(client, stars_filter=None):
    res = await fetch_store_gifts(client)
    gifts = list(getattr(res, "gifts", []) or [])
    if stars_filter is not None:
        gifts = [g for g in gifts if safe_int(getattr(g, "stars", 0)) == stars_filter]
    return gifts

async def print_store_gifts(client, stars_filter=None):
    gifts = await list_store_gifts(client, stars_filter=stars_filter)
    if not gifts:
        print("Nothing found in the shop using the filter.")
        return

    for i, g in enumerate(gifts, start=1):
        print(f"{i:>3}. {format_store_gift(g)}")
