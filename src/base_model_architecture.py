import sys
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Activation, BatchNormalization, Input, 
    Embedding, Dot, Dense, Flatten
)
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from utils.common_functions import read_yaml
from src.custom_exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)

class BaseModel:
    def __init__(self, config_path):
        try:
            self.config_path = read_yaml(config_path)
            logger.info('Loaded configuration from config.yaml')

        except Exception as e:
            logger.error(f'Error loading configuration {e}')
            raise CustomException('Error loading configuration', sys)
        

    def model_architecture(self, num_users, num_animes):
        try:
            embedding_size = self.config_path['model']['embedding_size']
            
            user = Input(name= 'user', shape= [1])
            user_embedding = Embedding(name= 'user_embedding', input_dim= num_users, output_dim= embedding_size)(user)


            anime = Input(name= 'anime', shape= [1])
            anime_embedding = Embedding(name= 'anime_embedding', input_dim= num_animes, output_dim= embedding_size)(anime)


            dot_product = Dot(name= 'dot_product', normalize= True, axes= 2)([user_embedding, anime_embedding])


            dot_product = Flatten()(dot_product)
            

            dot_product = Dense(1, kernel_initializer= 'he_normal')(dot_product)


            dot_product = BatchNormalization()(dot_product)


            dot_product = Activation('sigmoid')(dot_product)


            model = Model(inputs= [user, anime], outputs= dot_product)


            model.compile(
                loss= self.config_path['model']['loss'],
                metrics= self.config_path['model']['metrics'],
                optimizer= self.config_path['model']['optimizer']
            )

            logger.info('Model created sucessfully')
            return model
        
        except Exception as e:
            logger.error(f'error when trying to create the model {e}')
            raise CustomException('error when trying to create the model', sys)
