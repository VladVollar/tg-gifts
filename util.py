def safe_int(v, default=0):
    try:
        return int(v)
    except Exception:
        return default

def get_doc_from_gift(gift_obj):
    if gift_obj is None:
        return None

    doc = getattr(gift_obj, "document", None)
    if doc:
        return doc

    sticker = getattr(gift_obj, "sticker", None)
    if sticker:
        return sticker

    st = getattr(gift_obj, "sticker", None)
    if st and getattr(st, "document", None):
        return st.document

    return None

def get_alt_from_document(doc):
    if not doc:
        return None
    for a in getattr(doc, "attributes", []) or []:
        if hasattr(a, "alt") and a.alt:
            return a.alt
    return None

def gift_label_from_star_gift(star_gift):
    title = getattr(star_gift, "title", None)
    if title:
        return title
    doc = get_doc_from_gift(star_gift)
    alt = get_alt_from_document(doc)
    if alt:
        return alt
    return "<no title/alt>"

def print_header(title: str):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

def input_int(prompt: str):
    return int(input(prompt).strip())

def input_str(prompt: str):
    return input(prompt).strip()
