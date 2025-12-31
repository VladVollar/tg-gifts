from util import get_doc_from_gift, get_alt_from_document
from store import list_store_gifts
from profile import find_saved_by_gift_id

async def download_from_profile_by_gift_id(client, gift_id: int, out_file: str):
    saved = await find_saved_by_gift_id(client, gift_id)
    if not saved:
        raise RuntimeError("Not found in profile: gift_id is missing from SavedStarGifts.")

    gift = getattr(saved, "gift", None)
    doc = get_doc_from_gift(gift)
    if not doc:
        raise RuntimeError("There is no sticker/document to download for this gift.")

    path = await client.download_media(doc, file=out_file)
    alt = get_alt_from_document(doc)
    return path, alt

async def download_from_store_by_gift_id(client, gift_id: int, out_file: str):
    gifts = await list_store_gifts(client, stars_filter=None)
    g = next((x for x in gifts if getattr(x, "id", None) == gift_id), None)
    if not g:
        raise RuntimeError("Not found in store: gift_id is missing from getStarGifts.")

    doc = get_doc_from_gift(g)
    if not doc:
        raise RuntimeError("This gift does not have a sticker/document available for download in the shop (or the type is hidden).")

    path = await client.download_media(doc, file=out_file)
    alt = get_alt_from_document(doc)
    return path, alt
