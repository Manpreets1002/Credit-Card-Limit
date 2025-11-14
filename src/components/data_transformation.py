from src.logger import logging
from src.utils import TIME
from src.exception import CustomException

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

TARGET_NAME = "Limit"

@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join("artifacts",TIME,"preprocessor","raw_data.csv")

class DataTransformation:
    def __init__(self):
        self.transform_config = DataTransformationConfig()

    def preprocessor_pipeline(self,df:pd.DataFrame):
        cat_col = df.select_dtypes(include="O").columns
        num_col = df.select_dtypes(exclude="O").columns

    def transformation_pipeline(self,train_path,test_path):
        try:
            logging.info("Transformation Pipeline Started")    
            train_data = pd.read_csv(train_path)
            logging.info("Train Data Read Successfully")

            test_data = pd.read_csv(test_path)
            logging.info("Test Data Read Successfully")

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