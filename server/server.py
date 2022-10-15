from os import path
from flask import *
from flask_cors import CORS
from model_manager import ModelManager

app = Flask(__name__)

CORS(app,supports_credentials=True)

BASE_MODEL_PATH = "ml\\trained_models"

model_weights_path = path.join(BASE_MODEL_PATH,"text_moderation_model_gc.h5")
model_structure_path = path.join(BASE_MODEL_PATH,"text_moderation_structure_gc.json")
text_vectorizer_path = path.join(BASE_MODEL_PATH,"text_vectorizer.pkl")

model = ModelManager(model_weights_path,model_structure_path,text_vectorizer_path)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

@app.route("/predict",methods=['POST'])
def predict_text():
    content = request.json
    result = model.predict_text(str(content['text']))
    return result.tolist()

if __name__ == "__main__":
  app.run(host='127.0.0.1', port=5000, debug=True)