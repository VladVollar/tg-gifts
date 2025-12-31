from telethon.tl import functions, types
from telethon.errors import RPCError

async def probe_payment_form(client, peer, gift_id: int):
    invoice = types.InputInvoiceStarGift(peer=peer, gift_id=gift_id)
    form = await client(functions.payments.GetPaymentFormRequest(
        invoice=invoice,
        theme_params=None
    ))
    return form, invoice

async def buy_gift_with_confirmation(client, gift_id: int, peer_entity, confirm_phrase: str = "BUY"):
    peer = await client.get_input_entity(peer_entity)

    try:
        form, invoice = await probe_payment_form(client, peer, gift_id)
    except RPCError as e:
        raise RuntimeError(f"Failed to obtain payment form: {e.__class__.__name__}: {e}")

    form_id = getattr(form, "form_id", None)

    print("\nPAYMENT FORM received.")
    print("gift_id:", gift_id)
    print("form_id:", form_id)
    print("peer:", peer_entity)
    print(f"To PURCHASE, please enter exactly: {confirm_phrase}")
    typed = input("> ").strip()

    if typed != confirm_phrase:
        print("Cancelled. No purchase was made.")
        return None

    try:
        res = await client(functions.payments.SendStarsFormRequest(
            form_id=form_id,
            invoice=invoice
        ))
        return res
    except RPCError as e:
        raise RuntimeError(f"Error during payment: {e.__class__.__name__}: {e}")
