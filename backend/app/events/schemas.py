"""Event schemas for Kafka streaming pipeline."""
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class EventType(str, Enum):
    ARTIST_CREATED = "artist.created"
    ARTIST_UPDATED = "artist.updated"
    ARTIST_DELETED = "artist.deleted"
    USER_REGISTERED = "user.registered"
    USER_UPDATED = "user.updated"
    RATING_CREATED = "rating.created"
    RATING_UPDATED = "rating.updated"
    PORTFOLIO_UPLOADED = "portfolio.uploaded"
    FAVORITE_ADDED = "favorite.added"
    FAVORITE_REMOVED = "favorite.removed"


class TattooEvent(BaseModel):
    event_type: EventType
    entity_id: int
    timestamp: datetime
    payload: dict
    version: int = 1

    class Config:
        from_attributes = True


class ArtistEvent(TattooEvent):
    event_type: EventType = EventType.ARTIST_CREATED


class UserEvent(TattooEvent):
    event_type: EventType = EventType.USER_REGISTERED


class RatingEvent(TattooEvent):
    event_type: EventType = EventType.RATING_CREATED
