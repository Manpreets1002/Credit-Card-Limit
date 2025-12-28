import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException

class Training:
    def __init__(self):
        self.ingestion = DataIngestion()
        self.transformation = DataTransformation()
        self.trainer = ModelTrainer()

    def training(self):
        try:
            train_path, test_path = self.ingestion.ingestion_pipeline()
            preprocessor_path = self.transformation.transformation_pipeline(train_path)
            self.trainer.model_training(preprocessor_path,train_path,test_path)
            return "Training Completed Succesfully"
        
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    train = Training()
    print("Training Started")
    train.training()
    print("Training Completed")