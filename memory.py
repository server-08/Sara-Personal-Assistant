"""SARA — Memory: last 10 messages (deque with auto-eviction)"""

from collections import deque

import config


class Memory:
    def __init__(self):
        # slot-0: system prompt (protected), slot-1..: chat history
        self._system = {"role": "system", "content": config.SYSTEM_PROMPT}
        self._history = deque(maxlen=config.MAX_HISTORY)

    def add(self, role: str, content: str) -> None:
        self._history.append({"role": role, "content": content})

    def get_messages(self) -> list:
        """System prompt + last N messages — API ko bhejne ke liye."""
        return [self._system] + list(self._history)

    def clear(self) -> None:
        """Sirf chat history reset — system prompt safe."""
        self._history.clear()
