from config.paths_config import *
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml

if __name__ == '__main__':
    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()


    model_training = ModelTraining(PROCESSED_DIR)
    model_training.train_model()