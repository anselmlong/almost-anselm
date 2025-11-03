from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel
import asyncio
import json
import os
from datetime import datetime
import pytz
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Load credentials
api_id = int(os.getenv("TG_API_ID") or os.getenv("TELEGRAM_API_ID") or 0)
api_hash = os.getenv("TG_API_HASH") or os.getenv("TELEGRAM_API_HASH")

# Selection defaults (tweak as needed)
MIN_MY_MSGS = 100
MAX_MEMBERS = 20  # ignore huge groups
TARGET_YEAR = 2025

# Paths (repo root relative)
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)
CANDIDATES_PATH = DATA_RAW / "chat_candidates.json"
FILTER_PATH = DATA_RAW / "chat_candidates.json"

from telethon import TelegramClient
client = TelegramClient('anon', api_id, api_hash)

def get_chat_name(entity):
    if hasattr(entity, "title") and entity.title:
        return entity.title
    if hasattr(entity, "first_name") and entity.first_name:
        return entity.first_name
    if hasattr(entity, "username") and entity.username:
        return entity.username
    return str(entity.id)


async def get_chat_filter_list(client):
    dialogs = await client.get_dialogs()

    candidates = []

    for dialog in dialogs:
        entity = dialog.entity

        # Skip broadcast channels
        if isinstance(entity, Channel) and entity.broadcast:
            continue

        # Skip very large groups
        participants = getattr(entity, "participants_count", None)
        if participants and participants > MAX_MEMBERS:
            continue

        # Count my messages to determine relevance + get last message date
        my_msg_count = 0
        last_date = None
        CUTOFF = datetime(TARGET_YEAR, 1, 1, tzinfo=pytz.UTC)
        async for msg in client.iter_messages(entity.id, from_user="me", limit=2000):
            if getattr(msg, "date", None):
                last_date = msg.date
                if msg.date < CUTOFF:
                    continue
            my_msg_count += 1
            # Only add if more than 100
            if my_msg_count >= MIN_MY_MSGS:
                candidate = {
					"id": int(entity.id),
					"name": get_chat_name(entity),
					"participants_count": participants,
					"my_msg_count": my_msg_count,
					"last_my_message_date": last_date.isoformat() if last_date else None,
					"type": type(entity).__name__,
				}
                print(type(entity), candidate["name"], participants, candidate["my_msg_count"])
                candidates.append(candidate)
                break


    # Write candidates to JSON so the user can manually filter/edit it.
    with open(CANDIDATES_PATH, "w") as fh:
        json.dump(candidates, fh, ensure_ascii=False, indent=2, default=str)

    print(f"Wrote {len(candidates)} chat candidates to {CANDIDATES_PATH}")
    print(f"Edit {FILTER_PATH} (list of chat ids) to select chats, then re-run pull_messages.")
    return candidates


async def pull_messages():
    client = TelegramClient("session", api_id, api_hash)
    await client.start()

    # Determine selected chat ids from FILTER_PATH. If it doesn't exist, generate candidates and exit.
    if not FILTER_PATH.exists():
        print(f"No filter file found at {FILTER_PATH}. Generating candidates...")
        await get_chat_filter_list(client)
        print("Please edit the filter file with a JSON list of chat ids (e.g. [12345, 67890]) and re-run this script.")
        await client.disconnect()
        return

    # Read filter file (expects a JSON array of chat ids)
    try:
        candidate_list = json.load(open(FILTER_PATH))
        # Expect either a JSON array of chat ids (e.g. [12345, 67890])
        # or an array of candidate dicts with an "id" key.
        selected_ids = []
        for c in candidate_list:
            if isinstance(c, dict) and "id" in c:
                selected_ids.append(int(c["id"]))
            else:
                raise ValueError(f"Unsupported filter entry: {c!r}")
    except Exception as e:
        print(f"Failed to read filter file {FILTER_PATH}: {e}")
        await client.disconnect()
        return

    print(f"✅ Using {len(selected_ids)} chat ids from {FILTER_PATH}")

    all_msgs = []

    for chat_id in selected_ids:
        print(f"📥 Pulling chat_id: {chat_id}")
        async for msg in client.iter_messages(chat_id, reverse=True, limit=5000):
            if not getattr(msg, "text", None):
                continue

            all_msgs.append({
                "chat_id": int(chat_id),
                "sender_id": getattr(msg, "sender_id", None),
                "text": msg.text,
                "date": str(getattr(msg, "date", None)),
                "is_out": getattr(msg, "out", False),
            })

    out_path = DATA_RAW / "messages.json"
    json.dump(all_msgs, open(out_path, "w"), ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(all_msgs)} messages → {out_path}")

    await client.disconnect()


if __name__ == "__main__":
    import sys

    # Usage: python pull_telegram.py scan  -> write candidates
    #        python pull_telegram.py pull  -> pull messages using data/raw/chat_filter.json
    if len(sys.argv) > 1 and sys.argv[1] in ("scan", "candidates"):
        # Create a short-lived client to scan chats
        async def _scan():
            client = TelegramClient("session", api_id, api_hash)
            await client.start()
            await get_chat_filter_list(client)
            await client.disconnect()

        asyncio.run(_scan())
    else:
        asyncio.run(pull_messages())
