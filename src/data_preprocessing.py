import os
import sys
import joblib
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir

        self.data_rating = None
        self.data_anime = None
        self.data_synopsis = None
        self.X_train_array = None
        self.X_test_array = None
        self.y_train = None
        self.y_test = None

        self.user2user_encoded = {}
        self.user2user_decoded = {}
        self.anime2anime_encoded = {}
        self.anime2anime_decoded = {}

        os.makedirs(self.output_dir, exist_ok=True)
        logger.info('Data Preprocessing Initialized')

    
    def load_data(self, usecols):
        try:
            logger.info('Starting the data loading process')

            self.data_rating = pd.read_csv(
                self.input_file, low_memory= True, usecols=usecols
            )
            
            logger.info('the data has been successfully uploaded')

        
        except Exception as e:
            logger.error(f'the data was not loaded successfully {e}')
            raise CustomException('the data was not loaded successfully', sys)
        

    def filter_users(self, min=400):
        try:
            logger.info('filtering users.........')
            ratings = self.data_rating['user_id'].value_counts()

            self.data_rating = self.data_rating[self.data_rating['user_id'].isin(ratings[ratings >= min].index)].copy()
            
            logger.info('users successfully filtered')

        
        except Exception as e:
            logger.error(f'failed to filter data {e}')
            raise CustomException('failed to filter data', sys)
        

    def min_max_scalerating(self):
        try:
            logger.info('This is the MinMaxScaler process.')
            min_rating = self.data_rating['rating'].min()
            max_rating = self.data_rating['rating'].max()

            self.data_rating['rating'] = self.data_rating['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values.astype(np.float64)

            logger.info('scaling done for Processing')


        except Exception as e:
            logger.error(f'filed to Scale data {e}')
            raise CustomException('failed to Scale data', sys)
        

    def encode_data(self):
        try:
            logger.info('starting decoding process')

            # Users
            user_ids = self.data_rating['user_id'].unique().tolist()
            self.user2user_encoded = {x: i for i, x in enumerate(user_ids)}
            self.user2user_decoded = {i: x for i, x in enumerate(user_ids)}
            self.data_rating['user'] = self.data_rating['user_id'].map(self.user2user_encoded)


            # Animes

            anime_ids = self.data_rating['anime_id'].unique().tolist()
            self.anime2anime_encoded = {x: i for i, x in enumerate(anime_ids)}
            self.anime2anime_decoded = {i: x for i, x in enumerate(anime_ids)}
            self.data_rating['anime'] = self.data_rating['anime_id'].map(self.anime2anime_encoded)


        except Exception as e:
            logger.error(f'failed to decoding data {e}')
            raise CustomException('failed to decoding data', sys)
        

    def split_data(self, test_size= 0.2, random_state= 42):
        try:
            logger.info('starting the division of data into training and testing')

            # separating into training and testing
            X = self.data_rating[['user', 'anime']].values
            y = self.data_rating['rating']

            # # Train Test Splitting
            X_train, X_test, self.y_train, self.y_test = train_test_split(
                X, y, random_state=random_state, shuffle=True, test_size=test_size
            )

            # # Splitting into two halves: user and anime
            self.X_train_array = [X_train[:, 0], X_train[:, 1]]
            self.X_test_array = [X_test[:, 0], X_test[:, 1]]

            logger.info('division done!')


        except Exception as e:
            logger.error(f'failed to split data {e}')
            raise CustomException('failed to split data', sys)
        

    def save_artifacts(self):
        try:
            artifacts = {
                'user2user_encoded': self.user2user_encoded,
                'user2user_decoded': self.user2user_decoded,
                'anime2anime_encoded': self.anime2anime_encoded,
                'anime2anime_decoded': self.anime2anime_decoded,
            }

            for name, data in artifacts.items():
                joblib.dump(data, os.path.join(self.output_dir, f'{name}.pkl'))

            joblib.dump(self.X_train_array, X_TRAIN_ARRAY)
            joblib.dump(self.X_test_array, X_TEST_ARRAY)
            joblib.dump(self.y_train, Y_TRAIN)
            joblib.dump(self.y_test, Y_TEST)

            self.data_rating.to_csv(DATA_RATING, index=False)

            logger.info('all training and test data, classified df, were saved')


        except Exception as e:
            logger.error(f'failed to save artifacts data {e}')
            raise CustomException('failed to save artifacts data', sys)
        

    def process_anime_data(self):
        try:
            self.data_anime = pd.read_csv('artifacts/raw/anime.csv', low_memory=True)
            self.data_anime = self.data_anime.replace("Unknown", np.nan)
            self.data_anime = self.data_anime.rename(
                            columns={
                                'MAL_ID': 'anime_id','English name': 'eng_version'
                            }
                        )

            self.data_anime['eng_version'] = self.data_anime['eng_version'].fillna(self.data_anime['Name'])

            # Sorting the datavalues
            self.data_anime.sort_values(
                by = ['Score'], inplace = True, ascending = False,
                kind = 'quicksort', na_position = 'last'
            )

            self.data_anime = self.data_anime[["anime_id", "eng_version", "Score", "Genres", "Episodes", "Type", "Premiered", "Members"]]

            # Anime Dataset with Synopsis
            cols= ['MAL_ID', 'Name', 'Genres', 'sypnopsis']
            self.data_synopsis = pd.read_csv(ANIMESYNOPSIS_CSV, usecols=cols)
            self.data_synopsis = self.data_synopsis.rename(
                                columns={
                                    'sypnopsis': 'synopsis',
                                    'MAL_ID': 'anime_id'
                                }
                            )
            
            # saving processed data sets
            self.data_anime.to_csv(DATA_ANIME, index=False)
            self.data_synopsis.to_csv(DATA_SYNOPSIS, index=False)

            logger.info('Anime and anime synopsis dataset successfully saved')

        except Exception as e:
            logger.error(f'failed to save anime ans synopsis data {e}')
            raise CustomException('failed to save anime ans synopsis data', sys)
        

    def run(self):
        try:
            logger.info('Starting the general race of data processing....')
            self.load_data(usecols=['user_id', 'anime_id', 'rating'])

            self.filter_users()

            self.min_max_scalerating()

            self.encode_data()

            self.split_data()

            self.save_artifacts()

            self.process_anime_data()
            logger.info('data processing run completed successfully')
        except Exception as e:
            logger.error(f'failure to execute the general data processing run {e}')
            raise CustomException('failure to execute the general data processing run', sys)


if __name__ == '__main__':
    data_processor = DataProcessor(ANIMELIST_CSV, PROCESSED_DIR)
    data_processor.run()