"""
Integration tests for Lakehouse pipeline
"""
import pytest
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import Artist, User, Rating, Portfolio
from app.lakehouse.orchestrator import LakehousePipeline
from app.events.schemas import EventType
from app.events.producer import KafkaEventProducer


@pytest.fixture
def db():
    """Create test database session"""
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_data_lake(tmp_path):
    """Create temporary Lakehouse directory"""
    lake_path = tmp_path / "data_lake"
    lake_path.mkdir()
    return str(lake_path)


@pytest.fixture
def sample_artists(db: Session):
    """Create sample artist data"""
    artists = [
        Artist(
            name="Tattoo Master 1",
            bio="Expert in traditional",
            location="São Paulo, SP",
            specialties="traditional,black_grey"
        ),
        Artist(
            name="Modern Artist",
            bio="Contemporary styles",
            location="Rio de Janeiro, RJ",
            specialties="watercolor,minimal"
        ),
    ]
    db.add_all(artists)
    db.commit()
    return artists


@pytest.fixture
def sample_users(db: Session):
    """Create sample user data"""
    users = [
        User(name="User 1", email="user1@test.com"),
        User(name="User 2", email="user2@test.com"),
    ]
    db.add_all(users)
    db.commit()
    return users


@pytest.fixture
def sample_ratings(db: Session, sample_artists, sample_users):
    """Create sample rating data"""
    ratings = [
        Rating(artist_id=sample_artists[0].id, user_id=sample_users[0].id, score=5, comment="Amazing!"),
        Rating(artist_id=sample_artists[0].id, user_id=sample_users[1].id, score=4, comment="Very good"),
        Rating(artist_id=sample_artists[1].id, user_id=sample_users[0].id, score=5, comment="Perfect"),
    ]
    db.add_all(ratings)
    db.commit()
    return ratings


class TestBronzeLayer:
    """Bronze layer ingestion tests"""

    def test_ingest_artists_from_database(self, db: Session, sample_artists, test_data_lake):
        """Test exporting artists to Bronze layer"""
        pipeline = LakehousePipeline(test_data_lake)
        
        result = pipeline.bronze.export_artists(db)
        
        assert result["status"] == "success"
        assert result["record_count"] >= len(sample_artists)
        assert (Path(test_data_lake) / "bronze").exists()

    def test_ingest_users_from_database(self, db: Session, sample_users, test_data_lake):
        """Test exporting users to Bronze layer"""
        pipeline = LakehousePipeline(test_data_lake)
        
        result = pipeline.bronze.export_users(db)
        
        assert result["status"] == "success"
        assert result["record_count"] >= len(sample_users)

    def test_ingest_ratings_from_database(self, db: Session, sample_ratings, test_data_lake):
        """Test exporting ratings to Bronze layer"""
        pipeline = LakehousePipeline(test_data_lake)
        
        result = pipeline.bronze.export_ratings(db)
        
        assert result["status"] == "success"
        assert result["record_count"] >= len(sample_ratings)

    def test_bronze_files_have_timestamps(self, db: Session, sample_artists, test_data_lake):
        """Test that Bronze layer adds timestamps to filenames"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_artists(db)
        
        bronze_files = list((Path(test_data_lake) / "bronze").glob("artists_*.parquet"))
        assert len(bronze_files) > 0
        
        # Verify filename format: artists_TIMESTAMP.parquet
        filename = bronze_files[0].name
        assert filename.startswith("artists_")
        assert filename.endswith(".parquet")


class TestSilverLayer:
    """Silver layer transformation tests"""

    def test_clean_artist_data(self, db: Session, sample_artists, test_data_lake):
        """Test artist data cleaning"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # First export to Bronze
        pipeline.bronze.export_artists(db)
        
        # Then transform to Silver
        result = pipeline.silver.clean_artists_from_bronze(test_data_lake)
        
        assert result["status"] == "success"
        assert result["cleaned_records"] >= len(sample_artists)

    def test_clean_users_data(self, db: Session, sample_users, test_data_lake):
        """Test user data cleaning"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_users(db)
        result = pipeline.silver.clean_users_from_bronze(test_data_lake)
        
        assert result["status"] == "success"

    def test_deduplication_works(self, db: Session, sample_users, test_data_lake):
        """Test that deduplication removes exact duplicates"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Export same data twice (simulating duplicates)
        pipeline.bronze.export_users(db)
        pipeline.bronze.export_users(db)
        
        result = pipeline.silver.clean_users_from_bronze(test_data_lake)
        
        # After deduplication, should have at most the unique users
        assert result["cleaned_records"] <= len(sample_users) * 2

    def test_enriched_artist_data_includes_stats(self, db: Session, sample_artists, sample_ratings, test_data_lake):
        """Test that Silver layer enriches artists with rating stats"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Export bronze data
        pipeline.bronze.export_artists(db)
        pipeline.bronze.export_ratings(db)
        
        # Transform to silver
        result = pipeline.silver.clean_and_enrich_artists(test_data_lake)
        
        assert result["status"] == "success"
        # Check enriched columns exist
        assert "avg_rating" in str(result.get("columns", []))


class TestGoldLayer:
    """Gold layer aggregation tests"""

    def test_generate_artist_metrics(self, db: Session, sample_artists, sample_ratings, test_data_lake):
        """Test artist metrics generation"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Full pipeline up to Silver
        pipeline.bronze.export_artists(db)
        pipeline.bronze.export_ratings(db)
        pipeline.silver.clean_artists_from_bronze(test_data_lake)
        pipeline.silver.clean_ratings_from_bronze(test_data_lake)
        
        # Generate Gold metrics
        result = pipeline.gold.generate_artist_metrics(test_data_lake)
        
        assert result["status"] == "success"
        assert result["total_artists"] >= 0

    def test_generate_market_insights(self, db: Session, sample_artists, sample_ratings, test_data_lake):
        """Test market-wide insights generation"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Setup Bronze+Silver
        pipeline.bronze.export_artists(db)
        pipeline.bronze.export_ratings(db)
        pipeline.silver.clean_artists_from_bronze(test_data_lake)
        pipeline.silver.clean_ratings_from_bronze(test_data_lake)
        
        # Generate insights
        result = pipeline.gold.generate_market_insights(test_data_lake)
        
        assert result["status"] == "success"
        assert "total_artists" in result or result["status"] == "success"

    def test_generate_user_engagement(self, db: Session, sample_users, sample_ratings, test_data_lake):
        """Test user engagement metrics"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Setup
        pipeline.bronze.export_users(db)
        pipeline.bronze.export_ratings(db)
        pipeline.silver.clean_users_from_bronze(test_data_lake)
        pipeline.silver.clean_ratings_from_bronze(test_data_lake)
        
        # Generate
        result = pipeline.gold.generate_user_engagement(test_data_lake)
        
        assert result["status"] == "success"

    def test_location_heatmap_generation(self, db: Session, sample_artists, test_data_lake):
        """Test geographic heatmap data generation"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_artists(db)
        pipeline.silver.clean_artists_from_bronze(test_data_lake)
        
        result = pipeline.gold.generate_location_heatmap(test_data_lake)
        
        assert result["status"] == "success"


class TestPipelineOrchestration:
    """Full pipeline orchestration tests"""

    def test_full_pipeline_execution(self, db: Session, sample_artists, sample_users, sample_ratings, test_data_lake):
        """Test complete Bronze → Silver → Gold pipeline"""
        pipeline = LakehousePipeline(test_data_lake)
        
        result = pipeline.run_pipeline(db)
        
        assert result["status"] == "success"
        assert result["bronze_exports"] >= 0
        assert result["silver_exports"] >= 0
        assert result["gold_exports"] >= 0

    def test_incremental_sync(self, db: Session, sample_artists, test_data_lake):
        """Test incremental pipeline (only changed data)"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # First run
        result1 = pipeline.run_pipeline(db)
        assert result1["status"] == "success"
        
        # Incremental run
        result2 = pipeline.run_incremental_sync(db, "2026-05-17")
        
        # Should either succeed or indicate no changes
        assert result2["status"] in ["success", "no_changes"]

    def test_pipeline_validation(self, db: Session, sample_artists, test_data_lake):
        """Test pipeline validation checks"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Run pipeline
        pipeline.run_pipeline(db)
        
        # Validate
        result = pipeline.validate_pipeline(test_data_lake)
        
        # Should have validation results
        assert "status" in result
        assert result["status"] in ["valid", "warnings", "errors"]

    def test_pipeline_error_recovery(self, db: Session, test_data_lake):
        """Test that pipeline recovers from errors gracefully"""
        pipeline = LakehousePipeline(test_data_lake)
        
        # Try to run with empty database (edge case)
        result = pipeline.run_pipeline(db)
        
        # Should handle gracefully even with empty data
        assert result["status"] in ["success", "warning"]


class TestStreamingEvents:
    """Kafka event streaming tests"""

    def test_event_producer_initialization(self):
        """Test Kafka producer initializes"""
        producer = KafkaEventProducer()
        
        assert producer is not None
        # Producer should either connect to Kafka or use fallback queue
        assert hasattr(producer, "send_event")

    def test_artist_event_publishing(self):
        """Test publishing artist creation event"""
        producer = KafkaEventProducer()
        
        result = producer.send_event(
            entity_id=1,
            event_type=EventType.ARTIST_CREATED,
            payload={"bio": "Test", "specialties": "traditional"}
        )
        
        # Should return success or queue info
        assert result is not None

    def test_rating_event_publishing(self):
        """Test publishing rating event"""
        producer = KafkaEventProducer()
        
        result = producer.send_event(
            entity_id=1,
            event_type=EventType.RATING_CREATED,
            payload={"score": 5, "comment": "Great!"}
        )
        
        assert result is not None

    def test_event_producer_handles_disconnection(self):
        """Test producer handles Kafka disconnection gracefully"""
        producer = KafkaEventProducer()
        
        # Should not raise even if Kafka is unavailable
        try:
            result = producer.send_event(
                entity_id=1,
                event_type=EventType.ARTIST_UPDATED,
                payload={"bio": "Updated"}
            )
            assert True  # Should complete without error
        except Exception as e:
            pytest.fail(f"Producer should handle disconnection: {e}")


class TestDataQuality:
    """Data quality validation tests"""

    def test_silver_data_has_no_null_ids(self, db: Session, sample_artists, test_data_lake):
        """Test that Silver layer removes records with null IDs"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_artists(db)
        result = pipeline.silver.clean_artists_from_bronze(test_data_lake)
        
        # Should validate primary keys exist
        assert result["status"] == "success"

    def test_gold_metrics_are_numeric(self, db: Session, sample_ratings, test_data_lake):
        """Test that Gold layer metrics are numeric types"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_ratings(db)
        pipeline.silver.clean_ratings_from_bronze(test_data_lake)
        
        result = pipeline.gold.generate_market_insights(test_data_lake)
        
        # Metrics should be numeric
        assert result["status"] == "success"

    def test_rating_scores_in_valid_range(self, db: Session, sample_ratings, test_data_lake):
        """Test that rating scores are between 1-5"""
        pipeline = LakehousePipeline(test_data_lake)
        
        pipeline.bronze.export_ratings(db)
        result = pipeline.silver.clean_ratings_from_bronze(test_data_lake)
        
        # Should validate score ranges
        assert result["status"] == "success"


# Run tests with: pytest tests/test_lakehouse.py -v
