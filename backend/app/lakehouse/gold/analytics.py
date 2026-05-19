"""Gold layer - aggregated metrics and KPIs for dashboards."""
from pathlib import Path
from datetime import datetime
import pandas as pd


class GoldLayer:
    def __init__(self, data_lake_path: str):
        self.data_lake_path = Path(data_lake_path)
        self.gold_path = self.data_lake_path / "gold"
        self.gold_path.mkdir(parents=True, exist_ok=True)

    def compute_artist_metrics(self, artists: pd.DataFrame, ratings: pd.DataFrame) -> pd.DataFrame:
        metrics = artists[["id", "user_id", "location", "years_experience"]].copy()
        
        rating_agg = ratings.groupby("artist_id").agg({
            "score": ["count", "mean", "min", "max"]
        }).reset_index()
        rating_agg.columns = ["id", "total_ratings", "avg_rating", "min_rating", "max_rating"]
        
        metrics = metrics.merge(rating_agg, on="id", how="left")
        metrics[["total_ratings", "avg_rating", "min_rating", "max_rating"]] = \
            metrics[["total_ratings", "avg_rating", "min_rating", "max_rating"]].fillna(0)
        
        metrics["rating_reliability"] = (
            metrics["total_ratings"].apply(lambda x: 1.0 if x >= 5 else 0.5 if x >= 1 else 0.0)
        )
        
        metrics["experience_bucket"] = pd.cut(
            metrics["years_experience"],
            bins=[0, 2, 5, 10, 100],
            labels=["novice", "intermediate", "advanced", "expert"]
        )
        
        return metrics

    def compute_market_insights(
        self,
        artists: pd.DataFrame,
        ratings: pd.DataFrame,
        users: pd.DataFrame
    ) -> pd.DataFrame:
        insights = {
            "total_artists": len(artists),
            "total_users": len(users),
            "total_reviews": len(ratings),
            "avg_rating_all": ratings["score"].mean() if len(ratings) > 0 else 0.0,
            "avg_experience_years": artists["years_experience"].mean(),
            "top_locations": artists["location"].value_counts().head(10).to_dict(),
            "rating_distribution": ratings["score"].value_counts().sort_index().to_dict(),
        }
        
        return pd.DataFrame([insights])

    def compute_user_engagement(self, ratings: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
        engagement = ratings.groupby("user_id").agg({
            "id": "count",
            "score": "mean"
        }).reset_index()
        engagement.columns = ["user_id", "total_reviews", "avg_rating_given"]
        
        engagement = engagement.merge(
            users[["id", "created_at"]],
            left_on="user_id",
            right_on="id",
            how="left"
        )
        engagement["created_at"] = pd.to_datetime(engagement["created_at"])
        engagement["days_active"] = (datetime.utcnow().date() - engagement["created_at"].dt.date).dt.days
        
        engagement = engagement.drop(columns=["id"])
        
        return engagement

    def compute_location_heatmap(self, artists: pd.DataFrame) -> pd.DataFrame:
        heatmap = artists[["latitude", "longitude", "location", "rating"]].copy()
        heatmap = heatmap.dropna(subset=["latitude", "longitude"])
        
        heatmap["density"] = 1
        location_grid = heatmap.groupby(["location"]).agg({
            "latitude": "mean",
            "longitude": "mean",
            "rating": "mean",
            "density": "count"
        }).reset_index()
        location_grid.columns = ["location", "lat_center", "lon_center", "avg_rating", "artist_count"]
        
        return location_grid

    def save_metrics(self, metric_name: str, df: pd.DataFrame) -> Path:
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        file_path = self.gold_path / f"{metric_name}_{timestamp}.parquet"
        df.to_parquet(file_path, index=False)
        return file_path

    def build_analytics(
        self,
        artists: pd.DataFrame,
        ratings: pd.DataFrame,
        users: pd.DataFrame
    ) -> dict[str, Path]:
        results = {
            "artist_metrics": self.save_metrics(
                "artist_metrics",
                self.compute_artist_metrics(artists, ratings)
            ),
            "market_insights": self.save_metrics(
                "market_insights",
                self.compute_market_insights(artists, ratings, users)
            ),
            "user_engagement": self.save_metrics(
                "user_engagement",
                self.compute_user_engagement(ratings, users)
            ),
            "location_heatmap": self.save_metrics(
                "location_heatmap",
                self.compute_location_heatmap(artists)
            ),
        }
        
        return results
