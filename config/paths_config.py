import os

############## DATA INGESTION ####################
RAW_DIR = 'artifacts/raw'
RAW_FILE_PATH = os.path.join(RAW_DIR, 'raw.csv')
CONFIG_PATH = 'config/config.yaml'


############### DATA PREPROCESSING ##################
PROCESSED_DIR = 'artifacts/processed'
ANIMELIST_CSV = 'artifacts/raw/animelist.csv'
ANIME_CSV = 'artifacts/raw/anime.csv'
ANIMESYNOPSIS_CSV = 'artifacts/raw/anime_with_synopsis.csv'

X_TRAIN_ARRAY = os.path.join(PROCESSED_DIR, 'X_train_array.pkl')
X_TEST_ARRAY = os.path.join(PROCESSED_DIR, 'X_test_array.pkl')
Y_TRAIN = os.path.join(PROCESSED_DIR, 'y_train.pkl')
Y_TEST = os.path.join(PROCESSED_DIR, 'y_test.pkl')

DATA_RATING = os.path.join(PROCESSED_DIR, 'data_rating.csv')
DATA_ANIME = os.path.join(PROCESSED_DIR, 'data_anime.csv')
DATA_SYNOPSIS = os.path.join(PROCESSED_DIR, 'data_synopsis.csv')

USER2USER_ENCODED = 'artifacts/processed/user2user_encoded.pkl'
USER2USER_DECODED = 'artifacts/processed/user2user_decoded.pkl'
ANIME2ANIME_ENCODED = 'artifacts/processed/anime2anime_encoded.pkl'
ANIME2ANIME_DECODED = 'artifacts/processed/anime2anime_decoded.pkl'


######################## MODEL TRAINING ########################
MODEL_DIR = 'artifacts/model'
WEIGHTS_DIR = 'artifacts/weights'
MODEL_PATH = os.path.join(MODEL_DIR, 'model.h5')
ANIMES_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, 'anime_weights.pkl')
USER_WEIGHTS_PATH = os.path.join(WEIGHTS_DIR, 'user_weights.pkl')
CHECKPOINT_FILE_PATH = 'artifacts/model_checkpoint/weights.weights.h5'