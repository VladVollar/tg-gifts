from telethon import TelegramClient

def make_client(api_id: int, api_hash: str, session_name: str = "tg"):
    return TelegramClient(session_name, api_id, api_hash)
