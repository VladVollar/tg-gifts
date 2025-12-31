import asyncio

from tg_client import make_client
from util import print_header, input_int, input_str
from store import print_store_gifts
from profile import print_profile_gifts
from download import download_from_profile_by_gift_id, download_from_store_by_gift_id
from purchase import probe_payment_form, buy_gift_with_confirmation

async def resolve_peer(client, peer_raw: str):
    peer_raw = (peer_raw or "").strip()
    if peer_raw == "" or peer_raw.lower() == "me":
        return await client.get_me()

    if peer_raw.startswith("@"):
        peer_raw = peer_raw[1:]

    try:
        # numeric id
        if peer_raw.isdigit():
            return await client.get_entity(int(peer_raw))
        return await client.get_entity(peer_raw)
    except Exception as e:
        raise RuntimeError(f"Could not find the recipient '{peer_raw}': {type(e).__name__}: {e}")

async def menu(client):
    while True:
        print_header("TG Gifts CLI")
        print("1) Shop: show all gifts")
        print("2) Shop: show gifts by price (stars)")
        print("3) Profile: show my gifts")
        print("4) Download animation (.tgs) by gift_id from profile")
        print("5) Download animation (.tgs) by gift_id from shop (if available in catalogue)")
        print("6) Check gift_id: get payment form (without purchase)")
        print("7) Buy gift by gift_id with confirmation (for yourself or someone else)")
        print("0) Exit")

        choice = input_str("\nChoice: ")

        if choice == "0":
            return

        if choice == "1":
            print_header("Store gifts (all)")
            await print_store_gifts(client)

        elif choice == "2":
            stars = input_int("Price (stars): ")
            print_header(f"Store gifts ({stars}⭐)")
            await print_store_gifts(client, stars_filter=stars)

        elif choice == "3":
            print_header("My profile gifts")
            await print_profile_gifts(client)

        elif choice == "4":
            gid = int(input_str("gift_id (from profile): "))
            out = input_str("File name (e.g. bear.tgs): ")
            print_header(f"Download from profile gift_id={gid}")
            path, alt = await download_from_profile_by_gift_id(client, gid, out)
            print("Downloaded:", path)
            print("alt:", alt)

        elif choice == "5":
            gid = int(input_str("gift_id (from the shop): "))
            out = input_str("File name (e.g. store.tgs): ")
            print_header(f"Download from store gift_id={gid}")
            path, alt = await download_from_store_by_gift_id(client, gid, out)
            print("Downloaded:", path)
            print("alt:", alt)

        elif choice == "6":
            gid = int(input_str("gift_id for verification: "))
            peer_raw = input_str("To (me / @username / id / phone) [me]: ")
            peer_entity = await resolve_peer(client, peer_raw or "me")
            peer = await client.get_input_entity(peer_entity)

            print_header(f"Probe payment form gift_id={gid}")
            form, _invoice = await probe_payment_form(client, peer, gid)
            print("OK: payment form issued.")
            print("form_id:", getattr(form, "form_id", None))

        elif choice == "7":
            gid = int(input_str("gift_id for purchase: "))
            peer_raw = input_str("To (me / @username / id / phone) [me]: ")
            peer_entity = await resolve_peer(client, peer_raw or "me")

            print_header(f"Buy gift_id={gid}")
            res = await buy_gift_with_confirmation(client, gid, peer_entity, confirm_phrase="BUY")
            if res is not None:
                print("Successfully. Answer:", type(res).__name__)

        else:
            print("Unknown menu item.")

        input("\nPress Enter to continue...")

async def main():
    api_id = int(input("api_id: ").strip())
    api_hash = input("api_hash: ").strip()

    client = make_client(api_id, api_hash, session_name="tg")
    async with client:
        await client.start()
        await menu(client)

if __name__ == "__main__":
    asyncio.run(main())
