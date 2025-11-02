"""Simple per-user memory store for the bot.

This is a minimal file-backed memory store for development/testing.
"""

from pathlib import Path
import json


class BotMemory:
    def __init__(self, dirpath: str = ".bot_memory"):
        self.dir = Path(dirpath)
        self.dir.mkdir(parents=True, exist_ok=True)

    def save(self, user_id: str, messages: list):
        (self.dir / f"{user_id}.json").write_text(json.dumps(messages))

    def load(self, user_id: str):
        p = self.dir / f"{user_id}.json"
        if not p.exists():
            return []
        return json.loads(p.read_text())


if __name__ == "__main__":
    m = BotMemory()
    m.save("u1", ["hello"]) 
    print(m.load("u1"))
