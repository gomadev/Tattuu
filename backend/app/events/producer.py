"""Kafka event producer for real-time data streaming."""
import json
import logging
from typing import Optional
from datetime import datetime
from app.events.schemas import EventType, TattooEvent
from app.core.config import get_settings

logger = logging.getLogger("kafka")
settings = get_settings()

try:
    from kafka import KafkaProducer
    from kafka.errors import KafkaError
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("Kafka not available, events will be queued locally")


class EventProducer:
    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self.producer = None
        self.events_topic = settings.KAFKA_EVENTS_TOPIC

        if KAFKA_AVAILABLE:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers.split(","),
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    acks="all",
                    retries=3,
                )
                logger.info(f"Kafka producer initialized: {self.bootstrap_servers}")
            except KafkaError as e:
                logger.error(f"Failed to initialize Kafka producer: {str(e)}")
                self.producer = None

    def send_event(self, event: TattooEvent) -> bool:
        if not self.producer:
            logger.warning(f"Event queued locally (Kafka unavailable): {event.event_type}")
            return False

        try:
            future = self.producer.send(
                self.events_topic,
                value=event.model_dump()
            )
            future.get(timeout=10)
            logger.debug(f"Event sent: {event.event_type} for entity {event.entity_id}")
            return True

        except KafkaError as e:
            logger.error(f"Failed to send event: {str(e)}")
            return False

    def send_batch_events(self, events: list[TattooEvent]) -> int:
        sent_count = 0
        for event in events:
            if self.send_event(event):
                sent_count += 1
        return sent_count

    def close(self) -> None:
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer closed")


_producer_instance: Optional[EventProducer] = None


def get_event_producer() -> EventProducer:
    global _producer_instance
    if _producer_instance is None:
        _producer_instance = EventProducer()
    return _producer_instance


def publish_artist_event(
    entity_id: int,
    event_type: EventType,
    payload: dict
) -> bool:
    event = TattooEvent(
        event_type=event_type,
        entity_id=entity_id,
        timestamp=datetime.utcnow(),
        payload=payload
    )
    producer = get_event_producer()
    return producer.send_event(event)


def publish_rating_event(
    entity_id: int,
    event_type: EventType,
    payload: dict
) -> bool:
    event = TattooEvent(
        event_type=event_type,
        entity_id=entity_id,
        timestamp=datetime.utcnow(),
        payload=payload
    )
    producer = get_event_producer()
    return producer.send_event(event)
