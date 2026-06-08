from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from app.core.config import get_settings


@dataclass
class Turn:
    query: str
    intent: str
    reply: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class ConversationState:
    session_id: str
    turns: list[Turn] = field(default_factory=list)

    def append(self, query: str, intent: str, reply: str, max_turns: int = 6) -> None:
        self.turns.append(Turn(query=query, intent=intent, reply=reply))
        self.turns = self.turns[-max_turns:]

    @property
    def last_query(self) -> str:
        return self.turns[-1].query if self.turns else ""


class InMemoryStateStore:
    """Conversation store. Redis can replace this class in deployment."""

    def __init__(self) -> None:
        self._states: dict[str, ConversationState] = {}

    def get(self, session_id: str) -> ConversationState:
        if session_id not in self._states:
            self._states[session_id] = ConversationState(session_id=session_id)
        return self._states[session_id]

    def append(self, session_id: str, query: str, intent: str, reply: str) -> ConversationState:
        state = self.get(session_id)
        state.append(query=query, intent=intent, reply=reply)
        return state


class RedisStateStore:
    """Redis-backed conversation store for AutoDL or server deployment."""

    def __init__(self, redis_url: str, ttl_seconds: int = 600) -> None:
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError("Redis backend requires: pip install redis") from exc
        self._client = redis.Redis.from_url(redis_url, decode_responses=True)
        self._ttl_seconds = ttl_seconds

    def get(self, session_id: str) -> ConversationState:
        raw = self._client.get(self._key(session_id))
        if not raw:
            return ConversationState(session_id=session_id)
        data = json.loads(raw)
        turns = [Turn(**turn) for turn in data.get("turns", [])]
        return ConversationState(session_id=session_id, turns=turns)

    def append(self, session_id: str, query: str, intent: str, reply: str) -> ConversationState:
        state = self.get(session_id)
        state.append(query=query, intent=intent, reply=reply)
        payload = {"session_id": state.session_id, "turns": [turn.__dict__ for turn in state.turns]}
        self._client.set(self._key(session_id), json.dumps(payload, ensure_ascii=False), ex=self._ttl_seconds)
        return state

    def _key(self, session_id: str) -> str:
        return f"vehicle-dialog:session:{session_id}"


def create_state_store() -> InMemoryStateStore | RedisStateStore:
    settings = get_settings()
    if settings.state_backend.lower() == "redis":
        return RedisStateStore(settings.redis_url)
    return InMemoryStateStore()
