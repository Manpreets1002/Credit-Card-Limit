from src.logger import logging
from src.utils import TIME
from src.exception import CustomException

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts",TIME,"data","raw_data.csv")
    train_data_path: str = os.path.join("artifacts",TIME,"data","train_data.csv")
    test_data_path: str = os.path.join("artifacts",TIME,"data","test_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def ingestion_pipeline(self):
        try:
            logging.info("Ingestion Pipeline Started")    
            df = pd.read_csv("C:\\Users\\HP\\Github\\Credit-Card-Limit\\data\\credit.csv")
            logging.info("Data Read Successfully")

            df.to_csv(self.ingestion_config.raw_data_path)
            logging.info("Raw Data Saved")

            train_data,test_data = train_test_split(df,random_state=42,test_size=0.8)

            train_data.to_csv(self.ingestion_config.train_data_path)
            logging.info("Train Data Saved")

            test_data.to_csv(self.ingestion_config.test_data_path)
            logging.info("Test Data Saved")

            logging.info("All data saved successfully")
            logging.info("Ingestion Pipeline Completed")

            return self.ingestion_config.train_data_path,self.ingestion_config.test_data_path
        except Exception as e:
            raise CustomException(e,sys)