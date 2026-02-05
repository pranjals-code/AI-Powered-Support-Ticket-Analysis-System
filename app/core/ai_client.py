from __future__ import annotations

import logging
from typing import Optional

import httpx

from app.core.config import settings
from app.core.enums import TicketCategory, TicketPriority

logger = logging.getLogger(__name__)


class AIClassificationResult:
    def __init__(
        self,
        priority: TicketPriority,
        category: TicketCategory,
        team: Optional[str],
        confidence: Optional[float],
    ):
        self.priority = priority
        self.category = category
        self.team = team
        self.confidence = confidence


async def classify_ticket(
    title: str,
    description: str,
) -> Optional[AIClassificationResult]:
    url = settings.ai_service_url.rstrip("/") + "/predict"
    payload = {"title": title, "description": description}

    try:
        async with httpx.AsyncClient(
            timeout=settings.ai_service_timeout_seconds
        ) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        logger.warning("AI service classification failed: %s", exc)
        return None

    try:
        priority = TicketPriority(data["priority"])
        category = TicketCategory(data["category"])
    except Exception as exc:
        logger.warning("AI service returned invalid data: %s", exc)
        return None

    return AIClassificationResult(
        priority=priority,
        category=category,
        team=data.get("team"),
        confidence=data.get("confidence"),
    )


def classify_ticket_sync(
    title: str,
    description: str,
) -> Optional[AIClassificationResult]:
    url = settings.ai_service_url.rstrip("/") + "/predict"
    payload = {"title": title, "description": description}

    try:
        with httpx.Client(timeout=settings.ai_service_timeout_seconds) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        logger.warning("AI service classification failed: %s", exc)
        return None

    try:
        priority = TicketPriority(data["priority"])
        category = TicketCategory(data["category"])
    except Exception as exc:
        logger.warning("AI service returned invalid data: %s", exc)
        return None

    return AIClassificationResult(
        priority=priority,
        category=category,
        team=data.get("team"),
        confidence=data.get("confidence"),
    )
