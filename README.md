# Telegram Star Gifts CLI

A command-line tool built on **Telethon (MTProto)** that allows you to
inspect, download, and purchase Telegram **Star Gifts**, including gifts
that are **hidden from the Telegram UI but still available via API**.

This project provides full visibility and control over Telegram Star
Gifts for your own account.

------------------------------------------------------------------------

## Features

-   📦 List **store gifts** (Stars catalog)
-   👤 List **profile gifts** (received/saved gifts)
-   🎞 Download gift animations (`.tgs` Telegram animated stickers)
-   🧪 Probe gift availability (get payment form without buying)
-   💫 Buy gifts with Stars (explicit confirmation required)
-   🎯 Supports gifts removed from UI but still accepted by the server

All purchase actions are protected with **manual confirmation** to
prevent accidental spending.

------------------------------------------------------------------------

## Requirements

-   Python **3.10+**
-   Telegram account with Stars balance
-   Telegram **API ID** and **API Hash**

Get your API credentials here:\
https://my.telegram.org → **API development tools**

------------------------------------------------------------------------

## Installation

``` bash
pip install -r requirements.txt
```

`requirements.txt`:

``` txt
telethon>=1.40.0
```

------------------------------------------------------------------------

## First Run & Authentication

``` bash
python main.py
```

On first launch, Telethon will ask for: - phone number - login code -
2FA password (if enabled)

A `tg.session` file will be created and reused on future runs.

------------------------------------------------------------------------

## Project Structure

    tg-gifts-cli/
    │
    ├── main.py          # Interactive CLI menu
    ├── tg_client.py     # TelegramClient factory
    ├── store.py         # Store (catalog) logic
    ├── profile.py       # Profile / saved gifts logic
    ├── download.py      # Download .tgs animations
    ├── purchase.py      # Payment & purchase logic
    ├── util.py          # Helpers and formatters
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## CLI Menu

    1) Store: list all gifts
    2) Store: list gifts by price (stars)
    3) Profile: list my gifts
    4) Download animation (.tgs) from profile by gift_id
    5) Download animation (.tgs) from store by gift_id
    6) Probe gift_id (get payment form, no purchase)
    7) Buy gift by gift_id (confirmation required)
    0) Exit

------------------------------------------------------------------------

## Downloading Gift Animations

Downloaded files are **Telegram animated stickers (`.tgs`)**.

### How to view `.tgs`

-   Send the file to **Saved Messages** in Telegram Desktop
-   Or convert `.tgs` → `.gif` / `.webm` using a converter

------------------------------------------------------------------------

## Purchasing Gifts

Purchases are performed using Telegram Stars via MTProto:

-   `payments.GetPaymentFormRequest`
-   `payments.SendStarsFormRequest`

Before completing a purchase, the CLI will: 1. Fetch the payment form 2.
Display gift and recipient information 3. Require **exact confirmation
input** (`BUY`)

No confirmation → no purchase.

------------------------------------------------------------------------

## Hidden / Removed Gifts

Telegram may: - remove gifts from the UI - but still allow purchases via
MTProto if the server accepts the `gift_id`

This tool allows you to: - extract `gift_id` from your profile - probe
availability - purchase gifts even if they are no longer visible in the
app

------------------------------------------------------------------------

## Security Notes

-   **Never share your `api_hash`**
-   If it was exposed, regenerate it immediately
-   This tool uses official MTProto methods, but you are responsible for
    complying with Telegram Terms of Service

------------------------------------------------------------------------

## Disclaimer

This project is for **educational and personal use** only.\
Telegram may change APIs, schemas, or gift availability at any time.

Use at your own risk.
