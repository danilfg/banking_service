from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def configure_logging(service_name: str) -> None:
    """Единая настройка структурированных логов для сервисов."""

    timestamper = structlog.processors.TimeStamper(fmt="iso")

    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.add_log_name,
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    structlog.get_logger().bind(service=service_name)


def get_logger() -> "structlog.stdlib.BoundLogger":
    return structlog.get_logger()


class KafkaLogSink:
    """Заглушка для отправки логов в Kafka -> Splunk."""

    def __init__(self, producer: Any | None = None, topic: str = "logs.app") -> None:
        self._producer = producer
        self._topic = topic

    async def write(self, payload: dict[str, Any]) -> None:
        if self._producer is None:
            return
        await self._producer.send_and_wait(self._topic, payload)
