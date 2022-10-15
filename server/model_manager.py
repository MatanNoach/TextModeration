from os import getcwd
import tensorflow as tf
from keras.models import model_from_json
from keras.layers import TextVectorization
from pathlib import Path
import numpy as np
import pickle
import preprocess

SEQUENCE_LENGTH = 1800
DATA_COLUMNS = ["comment_text"]


class ModelManager():
    def __init__(self,model_weights_path,model_structure_path,vectorizer_path) -> None:
        self.trained_model = self.load_full_model(model_weights_path,model_structure_path)
        self.vectorizer = self.load_text_vectorizer(vectorizer_path)

    def load_full_model(self,model_weights_path,model_structure_path):
        f = Path(model_structure_path)
        model_structure = f.read_text()
        trained_model = model_from_json(model_structure)
        trained_model.load_weights(model_weights_path)
        return trained_model
    
    def load_text_vectorizer(self,vectorizer_path):
        vectorizer_data = pickle.load(open(vectorizer_path,"rb"))
        vectorizer = TextVectorization.from_config(vectorizer_data['config'])
        vectorizer.set_weights(vectorizer_data['weights'])
        return vectorizer

    def preprocess_text(self,text) -> str:
        processed_text = preprocess.text_pipeline(text)
        return tf.reshape(self.vectorizer(processed_text),(1,SEQUENCE_LENGTH))


    def predict_text(self,text) -> np.array:
        text = self.preprocess_text(text)
        return self.trained_model.predict(text,batch_size=1).flatten()