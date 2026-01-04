from src.logger import logging
from src.exception import CustomException
from src.utils import get_path

import os
from dotenv import load_dotenv
from joblib import load


class Prediction:
    def __init__(self):
        self.preprocessor_path, self.model_path = get_path()
    
    def predict(self,income,rating,cards,age,education,gender,student,married,ethnicity,balance):
        preprocessor = load(self.preprocessor_path)
        model = load(self.model_path)

        data = [income,rating,cards,age,education,gender,student,married,ethnicity,balance]
        test_data = preprocessor.transform(data)

        predicted_data = model.predict(test_data)

        return predicted_data 