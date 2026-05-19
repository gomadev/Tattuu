"""Bronze layer - raw data ingestion from operational database and events."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd
from sqlalchemy.orm import Session
from app.models.models import User, Artist, Rating, Portfolio


class BronzeLayer:
    def __init__(self, data_lake_path: str):
        self.data_lake_path = Path(data_lake_path)
        self.bronze_path = self.data_lake_path / "bronze"
        self.bronze_path.mkdir(parents=True, exist_ok=True)

    def export_users(self, db: Session) -> pd.DataFrame:
        users = db.query(User).all()
        data = [
            {
                "id": u.id,
                "email": u.email,
                "username": u.username,
                "full_name": u.full_name,
                "is_active": u.is_active,
                "created_at": u.created_at,
                "updated_at": u.updated_at,
            }
            for u in users
        ]
        df = pd.DataFrame(data)
        return df

    def export_artists(self, db: Session) -> pd.DataFrame:
        artists = db.query(Artist).all()
        data = [
            {
                "id": a.id,
                "user_id": a.user_id,
                "bio": a.bio,
                "location": a.location,
                "latitude": a.latitude,
                "longitude": a.longitude,
                "years_experience": a.years_experience,
                "rating": float(a.rating),
                "total_ratings": a.total_ratings,
                "created_at": a.created_at,
                "updated_at": a.updated_at,
            }
            for a in artists
        ]
        df = pd.DataFrame(data)
        return df

    def export_ratings(self, db: Session) -> pd.DataFrame:
        ratings = db.query(Rating).all()
        data = [
            {
                "id": r.id,
                "user_id": r.user_id,
                "artist_id": r.artist_id,
                "score": r.score,
                "comment": r.comment,
                "created_at": r.created_at,
                "updated_at": r.updated_at,
            }
            for r in ratings
        ]
        df = pd.DataFrame(data)
        return df

    def export_portfolios(self, db: Session) -> pd.DataFrame:
        portfolios = db.query(Portfolio).all()
        data = [
            {
                "id": p.id,
                "artist_id": p.artist_id,
                "title": p.title,
                "description": p.description,
                "image_url": p.image_url,
                "style_id": p.style_id,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in portfolios
        ]
        df = pd.DataFrame(data)
        return df

    def save_raw_export(self, entity: str, df: pd.DataFrame) -> Path:
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        file_path = self.bronze_path / f"{entity}_{timestamp}.parquet"
        df.to_parquet(file_path, index=False)
        return file_path

    def ingest_event(self, event: dict) -> Path:
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        event_type = event.get("event_type", "unknown")
        file_path = self.bronze_path / f"events_{event_type}_{timestamp}.json"
        
        with open(file_path, "w") as f:
            json.dump(event, f)
        
        return file_path

    def export_all(self, db: Session) -> dict[str, Path]:
        exports = {
            "users": self.save_raw_export("users", self.export_users(db)),
            "artists": self.save_raw_export("artists", self.export_artists(db)),
            "ratings": self.save_raw_export("ratings", self.export_ratings(db)),
            "portfolios": self.save_raw_export("portfolios", self.export_portfolios(db)),
        }
        return exports
