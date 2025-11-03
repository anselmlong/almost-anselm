import os
import sys
from pathlib import Path

# Optionally load a local .env file if python-dotenv is available.
try:
    from dotenv import load_dotenv
    # Look for a .env in the repository root (two levels up from this file)
    repo_root = Path(__file__).resolve().parents[2]
    dotenv_path = repo_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
    else:
        # fallback to default load (looks in CWD and parent dirs)
        load_dotenv()
except Exception:
    # If python-dotenv isn't installed or loading fails, continue; env vars may be set externally.
    pass

# Remember to use your own values from my.telegram.org!
# Try multiple common env var names for flexibility.
api_id_str = os.getenv("TG_API_ID") or os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TG_API_HASH") or os.getenv("TELEGRAM_API_HASH")

if not api_id_str or not api_hash:
    sys.stderr.write(
        "Error: Telegram API credentials are missing.\n"
        "Set TG_API_ID and TG_API_HASH in your environment (see README or my.telegram.org).\n"
        "Example:\n  export TG_API_ID=123456\n  export TG_API_HASH=yourhashhere\n"
    )
    sys.exit(2)

try:
    api_id = int(api_id_str)
except ValueError:
    sys.stderr.write("Error: TG_API_ID must be an integer.\n")
    sys.exit(2)

from telethon import TelegramClient
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

    # You can send messages to yourself...
    await client.send_message('me', 'Hello, myself!')
    # ...to some chat ID
    # ...to your contacts
    # ...or even to any username
    await client.send_message('@verity38', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # Sending a message returns the sent message object, which you can use
    print(message.raw_text)

    # You can reply to messages directly if you have a message object
    await message.reply('Cool!')

    # Or send files, songs, documents, albums...

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(main())