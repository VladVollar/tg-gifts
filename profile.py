from telethon.tl import functions
from util import safe_int, gift_label_from_star_gift

async def iter_profile_gifts(client, limit=100):
    offset = ""
    while True:
        res = await client(functions.payments.GetSavedStarGiftsRequest(
            peer="me",
            offset=offset,
            limit=limit,
        ))

        items = list(getattr(res, "gifts", []) or [])
        for it in items:
            yield it

        next_offset = getattr(res, "next_offset", None)
        if not next_offset or next_offset == offset:
            break
        offset = next_offset

def format_saved_star_gift(saved):
    gift = getattr(saved, "gift", None)
    if not gift:
        return "SavedStarGift: <no gift>"

    gid = getattr(gift, "id", None)
    stars = safe_int(getattr(gift, "stars", 0))
    label = gift_label_from_star_gift(gift)

    flags = []
    if getattr(saved, "unsaved", False): flags.append("UNSAVED")
    if getattr(saved, "pinned_to_top", False): flags.append("PINNED")
    if getattr(saved, "refunded", False): flags.append("REFUNDED")

    msg_id = getattr(saved, "msg_id", None)
    date = getattr(saved, "date", None)

    meta = []
    if msg_id is not None: meta.append(f"msg_id={msg_id}")
    if date is not None: meta.append(f"date={date}")

    return f"gift_id={gid} | {stars}⭐ | {label}" + (f" | {' '.join(flags)}" if flags else "") + (f" | {' '.join(meta)}" if meta else "")

async def print_profile_gifts(client):
    i = 0
    async for saved in iter_profile_gifts(client):
        i += 1
        print(f"{i:>3}. {format_saved_star_gift(saved)}")

    if i == 0:
        print("Not found in the gift profile (or the method returned empty).")

async def find_saved_by_gift_id(client, gift_id: int):
    async for saved in iter_profile_gifts(client):
        gift = getattr(saved, "gift", None)
        if gift and getattr(gift, "id", None) == gift_id:
            return saved
    return None
