import os
import sys
import pandas as pd
from google.cloud import storage
from config.paths_config import *
from utils.common_functions import read_yaml
from src.custom_exception import CustomException
from src.logger import get_logger


logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]


        os.makedirs(RAW_DIR, exist_ok= True)

        logger.info(
            f'Data ingestion started with {self.bucket_name}, file name(s) is {self.bucket_file_name}'
        )


    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)

            for file_name in self.bucket_file_name:
                file_path = os.path.join(RAW_DIR, file_name)

                if file_name == 'animelist.csv':
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    data = pd.read_csv(file_path, nrows=5_000_000)
                    data.to_csv(file_path, index=False)
                    
                    logger.info(f'The large file was downloaded and filtered correctly, path:{file_path}')

                else:
                    blob = bucket.blob(file_name)
                    blob.download_to_filename(file_path)

                    logger.info(f'The smaller files were downloaded successfully, path: {file_path}')

        except Exception as e:
            logger.error(f'Error downloading csv file. Original exception: {e}', exc_info=True) 
            raise CustomException('Failed to perform csv file download', sys)
        

    def run(self):
        try:
            logger.info('Starting data ingestion process')

            self.download_csv_from_gcp()
            
            logger.info('Data ingestion completed succesfully')

        except CustomException as ce:
            logger.error(f"CustomerException: {str(ce)}")

        finally:
            logger.info("Data ingestion DONE")



if __name__ == '__main__':
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()