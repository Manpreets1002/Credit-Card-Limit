from src.logger import logging
from src.utils import TIME, upload_path
from src.exception import CustomException

import os
import sys
import pandas as pd
import joblib
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from dataclasses import dataclass

TARGET_NAME = "Credit_Limit"

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts",TIME,"models","catboost","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainerConfig()

    def model_training(self,preprocessor_path,train_path,test_path):
        try:
            df = pd.read_csv(train_path)
            logging.info("Data Read Successfully for model training")

            x = df.drop(TARGET_NAME,axis=1)
            y = df[TARGET_NAME]

            xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.2,random_state=42)
            logging.info("Data Splitted into xtrain and ytrain")

            preprocessor = joblib.load(preprocessor_path)
            logging.info("Preprocessor Read Successfully")

            xtrain_transformed = preprocessor.transform(xtrain)
            xtest_transformed = preprocessor.transform(xtest)
            logging.info("Data converted to model understandable language")

            model = CatBoostRegressor()
            model.fit(xtrain,ytrain)
            logging.info("Model Trained Successfully")
            ypred = model.predict(xtest)
            r2 = r2_score(ytest,ypred)
            logging.info(f"R2 Score of the Model: {r2}")

            joblib.dump(model,self.model_config.model_path)
            logging.info("Model Saved Successfully")

            logging.info("-"*60)
            logging.info("Testing with the Testing Dataframe")
            testing = pd.read_csv(test_path)
            target_testing = testing[TARGET_NAME]
            target_input = testing.drop(TARGET_NAME)

            target_noramlized_value = preprocessor.transform(target_input)

            predictions = model.predict(target_noramlized_value)
            r2_testing = r2_score(target_testing,predictions)
            logging.info(f"R2 Score of the Model: {r2_testing}")
            logging.info("Testing with the Testing Dataframe Done")
            logging.info("-"*60)

            upload_path(preprocessor_path,self.model_config.model_path)
            logging.info("Preporcessor and Model Path saved in the db")

        except Exception as e:
            raise CustomException(e,sys)