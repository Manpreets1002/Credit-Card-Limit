from src.logger import logging
from src.utils import TIME, connection_enable, connection_disable
from src.exception import CustomException

import os
import sys
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from dataclasses import dataclass

load_dotenv()

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts",TIME,"data","raw_data","data.csv")
    train_data_path: str = os.path.join("artifacts",TIME,"data","raw_data","train_data.csv")
    test_data_path: str = os.path.join("artifacts",TIME,"data","raw_data","test_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
        os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
        os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)

    def ingestion_pipeline(self):
        try:
            logging.info("Ingestion Pipeline Started")
            engine = connection_enable()
            logging.info("SQL Connection Enabled")

            conn = engine.connect()
            query = "SELECT * FROM credit;"

            df = pd.read_sql(query,conn)
            logging.info("Data Read Successfully")

            connection_disable(engine)
            logging.info("SQL Connection Disposed")

            df.to_csv(self.ingestion_config.raw_data_path)
            logging.info("Raw Data Saved")

            train_data,test_data = train_test_split(df,random_state=42,test_size=0.2)

            train_data.to_csv(self.ingestion_config.train_data_path)
            logging.info("Train Data Saved")

            test_data.to_csv(self.ingestion_config.test_data_path)
            logging.info("Test Data Saved")

            logging.info("All data saved successfully")
            logging.info("Ingestion Pipeline Completed")

            return self.ingestion_config.train_data_path,self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e,sys)