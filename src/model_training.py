import os
import sys
import joblib
import comet_ml
import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from src.custom_exception import CustomException
from src.logger import get_logger
from src.base_model_architecture import BaseModel
from config.paths_config import *

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, data_path):
        self.data_path = data_path

        self.experiment = comet_ml.Experiment(
            api_key='M6UVoXPUp9FNLNlvb4od99sev',
            project_name='mlops-project-2-recommendation-system',
            workspace= "zeyoliveira"
        )

        logger.info("Model training and Comet ML initialized")

    def load_data(self):
        try:
            X_train_array = joblib.load(X_TRAIN_ARRAY)
            X_test_array = joblib.load(X_TEST_ARRAY)
            y_train = joblib.load(Y_TRAIN)
            y_test = joblib.load(Y_TEST)

            logger.info('Data loaded sucesfully for Model Training')

            return X_train_array, X_test_array, y_train, y_test
        except Exception as e:
            logger.error(f'Faled to load data {e}')
            raise CustomException('Failed to load data', sys)

    def train_model(self):
        try:
            logger.info('training started')

            X_train_array, X_test_array, y_train, y_test = self.load_data()
            num_users = len(joblib.load(USER2USER_ENCODED))
            num_animes = len(joblib.load(ANIME2ANIME_ENCODED))

            base_model = BaseModel(config_path=CONFIG_PATH)
            model = base_model.model_architecture(num_users=num_users, num_animes=num_animes)

            # Required values for model training
            start_lr = 0.00001
            min_lr = 0.0001
            max_lr = 0.00005
            batch_size = 10000
            ram_epochs = 4
            sustain_epochs = 0
            exp_decay = 0.8

            #The purpose of this function is basically to find the best learning rate for the model.
            def learning_rate_fn(epoch):
                if epoch < ram_epochs:
                    return (max_lr - start_lr) / ram_epochs * epoch + start_lr
                elif epoch < ram_epochs + sustain_epochs:
                    return max_lr
                else:
                    return (max_lr - min_lr) * exp_decay ** (epoch - ram_epochs - sustain_epochs) + min_lr
                
            learning_rate_callback = LearningRateScheduler(
                lambda epoch: learning_rate_fn(epoch= epoch), verbose= 0
            )


            model_checkpoint = ModelCheckpoint(
                filepath= CHECKPOINT_FILE_PATH, save_weights_only= True, 
                monitor= 'val_loss', mode= 'min', save_best_only= True
            )


            early_stopping = EarlyStopping(
                patience= 5, monitor= 'val_loss', 
                mode= 'min', restore_best_weights= True
            )

                                                                            
            callbacks = [model_checkpoint, learning_rate_callback, early_stopping]  

            os.makedirs(os.path.dirname(CHECKPOINT_FILE_PATH), exist_ok=True)
            os.makedirs(MODEL_DIR, exist_ok=True)
            os.makedirs(WEIGHTS_DIR, exist_ok=True)

            try:
                historical = model.fit(
                                x= X_train_array,
                                y= y_train,
                                batch_size= batch_size,
                                epochs= 13,
                                verbose= 1,
                                validation_data= (X_test_array, y_test),
                                callbacks= callbacks
                            )
                model.load_weights(CHECKPOINT_FILE_PATH)
                logger.info('Model training completed')

                for epoch in range(len(historical.history['loss'])):
                    train_loss = historical.history['loss'][epoch]
                    val_loss = historical.history['val_loss'][epoch]

                    self.experiment.log_metric('train_loss', train_loss, step=epoch)
                    self.experiment.log_metric('val_loss', val_loss, step=epoch)



            except Exception as e:
                logger.error(f'Model training failed {e}')
                raise CustomException('Model training failed', sys)
            
            self.save_model_weights(model)

        except Exception as e:
            logger.error(str(e))
            raise CustomException('Error during model training process', sys)
        
    def extract_weights(self, layer_name, model):
        try:
            weight_layer = model.get_layer(layer_name)
            weights = weight_layer.get_weights()[0]
            weights = weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))
            logger.info(f'Extrating weights for {layer_name}')
            return weights
        except Exception as e:
            logger.error(str(e))
            raise CustomException('Error during weight extraction process', sys)
        
    def save_model_weights(self, model):
        try:
            model.save(MODEL_PATH)
            logger.info(f'Model save to {MODEL_PATH}')

            user_weights = self.extract_weights('user_embedding', model)
            anime_weights = self.extract_weights('anime_embedding', model)

            joblib.dump(user_weights, USER_WEIGHTS_PATH)
            joblib.dump(anime_weights, ANIMES_WEIGHTS_PATH)


            self.experiment.log_asset(MODEL_PATH)
            self.experiment.log_asset(USER_WEIGHTS_PATH)
            self.experiment.log_asset(ANIMES_WEIGHTS_PATH)

            logger.info('User and Anime weights saved sucessfully')


        except Exception as e:
            logger.error(str(e))
            raise CustomException('Error during weight save process', sys)



if __name__ == '__main__':
    model_training = ModelTraining(PROCESSED_DIR)
    model_training.train_model()