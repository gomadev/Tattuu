"""Silver layer - data cleaning, deduplication, and transformation."""
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np


class SilverLayer:
    def __init__(self, data_lake_path: str):
        self.data_lake_path = Path(data_lake_path)
        self.silver_path = self.data_lake_path / "silver"
        self.silver_path.mkdir(parents=True, exist_ok=True)

    def clean_users(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        df_clean = df_clean.drop_duplicates(subset=["id"], keep="last")
        df_clean["email"] = df_clean["email"].str.lower().str.strip()
        df_clean["username"] = df_clean["username"].str.strip()
        df_clean["created_at"] = pd.to_datetime(df_clean["created_at"])
        df_clean["updated_at"] = pd.to_datetime(df_clean["updated_at"])
        
        return df_clean

    def clean_artists(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        df_clean = df_clean.drop_duplicates(subset=["id"], keep="last")
        df_clean["location"] = df_clean["location"].str.strip()
        df_clean["years_experience"] = df_clean["years_experience"].fillna(0).astype(int)
        df_clean["rating"] = df_clean["rating"].fillna(0.0).astype(float)
        df_clean["total_ratings"] = df_clean["total_ratings"].fillna(0).astype(int)
        df_clean["created_at"] = pd.to_datetime(df_clean["created_at"])
        df_clean["updated_at"] = pd.to_datetime(df_clean["updated_at"])
        
        df_clean = df_clean[df_clean["latitude"].notna() & df_clean["longitude"].notna()]
        
        return df_clean

    def clean_ratings(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        df_clean = df_clean.drop_duplicates(subset=["id"], keep="last")
        df_clean["score"] = df_clean["score"].astype(int)
        df_clean["comment"] = df_clean["comment"].fillna("").str.strip()
        df_clean["created_at"] = pd.to_datetime(df_clean["created_at"])
        df_clean["updated_at"] = pd.to_datetime(df_clean["updated_at"])
        
        df_clean = df_clean[df_clean["score"].between(1, 5)]
        
        return df_clean

    def clean_portfolios(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        df_clean = df_clean.drop_duplicates(subset=["id"], keep="last")
        df_clean["title"] = df_clean["title"].str.strip()
        df_clean["description"] = df_clean["description"].fillna("").str.strip()
        df_clean["created_at"] = pd.to_datetime(df_clean["created_at"])
        df_clean["updated_at"] = pd.to_datetime(df_clean["updated_at"])
        
        return df_clean

    def enrich_artists(self, artists: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
        df_enriched = artists.copy()
        
        rating_stats = ratings.groupby("artist_id").agg({
            "score": ["mean", "std", "count"]
        }).reset_index()
        rating_stats.columns = ["id", "avg_score", "score_std", "total_reviews"]
        
        df_enriched = df_enriched.merge(rating_stats, on="id", how="left")
        df_enriched["avg_score"] = df_enriched["avg_score"].fillna(0.0)
        df_enriched["score_std"] = df_enriched["score_std"].fillna(0.0)
        df_enriched["total_reviews"] = df_enriched["total_reviews"].fillna(0).astype(int)
        
        return df_enriched

    def save_cleaned(self, entity: str, df: pd.DataFrame) -> Path:
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        file_path = self.silver_path / f"{entity}_cleaned_{timestamp}.parquet"
        df.to_parquet(file_path, index=False)
        return file_path

    def transform_bronze(self, bronze_exports: dict[str, Path]) -> dict[str, pd.DataFrame]:
        users_df = pd.read_parquet(bronze_exports["users"])
        artists_df = pd.read_parquet(bronze_exports["artists"])
        ratings_df = pd.read_parquet(bronze_exports["ratings"])
        portfolios_df = pd.read_parquet(bronze_exports["portfolios"])

        cleaned = {
            "users": self.clean_users(users_df),
            "artists": self.clean_artists(artists_df),
            "ratings": self.clean_ratings(ratings_df),
            "portfolios": self.clean_portfolios(portfolios_df),
        }

        cleaned["artists"] = self.enrich_artists(cleaned["artists"], cleaned["ratings"])

        return cleaned

    def save_all_cleaned(self, cleaned_data: dict[str, pd.DataFrame]) -> dict[str, Path]:
        saved = {}
        for entity, df in cleaned_data.items():
            saved[entity] = self.save_cleaned(entity, df)
        return saved
