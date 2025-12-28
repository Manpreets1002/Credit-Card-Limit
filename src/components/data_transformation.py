from src.logger import logging
from src.utils import TIME
from src.exception import CustomException

import os
import sys
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
import joblib

TARGET_NAME = "Credit_Limit"

@dataclass
class DataTransformationConfig:
    preprocessor_path: str = os.path.join("artifacts",TIME,"preprocessor","pipeline.pkl")

class DataTransformation:
    def __init__(self):
        self.transform_config = DataTransformationConfig()

    def preprocessor_pipeline(self,df:pd.DataFrame):
        try:
            logging.info("Pipeline Creation Started")
            cat_col = df.select_dtypes(include="O").columns
            num_col = df.select_dtypes(exclude="O").columns

            logging.info(f"Categorical Columns: {cat_col}")
            logging.info(f"Numerical Columns: {num_col}")

            num_pipeline = Pipeline(
                [
                    ("num_imputer",SimpleImputer(strategy="median")),
                    ("num_scaler",StandardScaler())
                ]
            )
            logging.info("Numerical Pipeline Created")

            cat_pipeline = Pipeline(
                [
                    ("cat_imputer",SimpleImputer(strategy="most_frequent")),
                    ("ohe",OneHotEncoder(handle_unknown="ignore")),
                    ("cat_ss",StandardScaler())
                ]
            )
            logging.info("Categorical Pipeline Created")

            pipeline = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_col),
                    ("cat_pipeline",cat_pipeline,cat_col)
                ],remainder="passthrough"
            )
            logging.info("Pipeline Created Successfully")

            return pipeline
        
        except Exception as e:
            raise CustomException(e,sys)

    def transformation_pipeline(self,train_data):
        try:
            logging.info("Transformation Pipeline Started")    
            train_data = pd.read_csv(train_data)
            logging.info("Data Read Successfully")

            df = train_data.drop(TARGET_NAME,axis=1)

            pipeline = self.preprocessor_pipeline(df)
            logging.info("Transformation Pipeline Successfully Fetched from the function")

            train_data_transformed = pipeline.fit_transform(df)
            logging.info("Pipeline Trained Successfully")

            joblib.dump(pipeline,self.transform_config.preprocessor_path)
            logging.info("Transformation Pipeline saved")

            return self.transform_config.preprocessor_path
        
        except Exception as e:
            raise CustomException(e,sys)