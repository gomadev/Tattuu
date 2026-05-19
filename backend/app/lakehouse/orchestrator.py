"""Lakehouse pipeline orchestrator."""
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.lakehouse.bronze import BronzeLayer
from app.lakehouse.silver import SilverLayer
from app.lakehouse.gold import GoldLayer

logger = logging.getLogger("lakehouse")


class LakehousePipeline:
    def __init__(self, data_lake_path: str):
        self.bronze = BronzeLayer(data_lake_path)
        self.silver = SilverLayer(data_lake_path)
        self.gold = GoldLayer(data_lake_path)

    def run_daily_batch(self, db: Session) -> dict:
        logger.info("Starting daily batch pipeline")
        start_time = datetime.utcnow()

        try:
            bronze_exports = self.bronze.export_all(db)
            logger.info(f"Bronze layer exports completed: {list(bronze_exports.keys())}")

            cleaned_data = self.silver.transform_bronze(bronze_exports)
            silver_exports = self.silver.save_all_cleaned(cleaned_data)
            logger.info(f"Silver layer transformations completed: {list(silver_exports.keys())}")

            gold_results = self.gold.build_analytics(
                cleaned_data["artists"],
                cleaned_data["ratings"],
                cleaned_data["users"]
            )
            logger.info(f"Gold layer analytics completed: {list(gold_results.keys())}")

            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()

            result = {
                "status": "success",
                "duration_seconds": duration,
                "bronze_exports": len(bronze_exports),
                "silver_exports": len(silver_exports),
                "gold_exports": len(gold_results),
            }

            logger.info(f"Daily batch completed successfully in {duration:.2f}s")
            return result

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise

    def run_incremental_sync(self, db: Session, last_sync: datetime) -> dict:
        logger.info(f"Starting incremental sync since {last_sync.isoformat()}")

        try:
            bronze_exports = self.bronze.export_all(db)
            cleaned_data = self.silver.transform_bronze(bronze_exports)
            silver_exports = self.silver.save_all_cleaned(cleaned_data)

            gold_results = self.gold.build_analytics(
                cleaned_data["artists"],
                cleaned_data["ratings"],
                cleaned_data["users"]
            )

            result = {
                "status": "success",
                "sync_time": last_sync.isoformat(),
                "records_processed": sum([
                    len(cleaned_data[k]) for k in cleaned_data.keys()
                ]),
            }

            logger.info(f"Incremental sync completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Incremental sync failed: {str(e)}", exc_info=True)
            raise
