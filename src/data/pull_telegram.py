"""Extract messages from Telegram using Telethon.

Placeholder module — implement Telethon logic here.
"""

from typing import List, Dict


def pull_messages(output_dir: str, limit: int = 10) -> List[Dict]:
    """Pull messages and save raw dumps to output_dir.

    Args:
        output_dir: directory to write raw dumps
        limit: maximum number of messages to fetch (for testing)

    Returns:
        A list of message dicts (placeholder)
    """
    # TODO: implement Telethon client, auth, and fetching
    return [{"id": i, "text": f"sample message {i}"} for i in range(limit)]


if __name__ == "__main__":
    print("This is a placeholder for pull_telegram.py")
