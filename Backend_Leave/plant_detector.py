import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load model and remedies only once
model = load_model('C:/Users/Administrator/Desktop/active/Leave_detection/Plant/best_model.h5')
remedies_df = pd.read_csv('C:/Users/Administrator/Desktop/active/Leave_detection/Plant/rotten_fruits_remedies.csv')

class_names = [
    'Apple__Healthy', 'Apple__Rotten',
    'Banana__Healthy', 'Banana__Rotten',
    'Bellpepper__Healthy', 'Bellpepper__Rotten',
    'Carrot__Healthy', 'Carrot__Rotten',
    'Cucumber__Healthy', 'Cucumber__Rotten',
    'Grape__Healthy', 'Grape__Rotten',
    'Guava__Healthy', 'Guava__Rotten',
    'Jujube__Healthy', 'Jujube__Rotten',
    'Mango__Healthy', 'Mango__Rotten',
    'Orange__Healthy', 'Orange__Rotten',
    'Pomegranate__Healthy', 'Pomegranate__Rotten',
    'Potato__Healthy', 'Potato__Rotten',
    'Strawberry__Healthy', 'Strawberry__Rotten',
    'Tomato__Healthy', 'Tomato__Rotten'
]

def get_result(file_path):
    img = image.load_img(file_path, target_size=(225, 225))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    confidence = float(prediction[0][predicted_index])
    if predicted_index >= len(class_names):
        return "Unknown", confidence
    return class_names[predicted_index], confidence

def get_remedy_info(fruit_class):
    match = remedies_df[remedies_df['Class'] == fruit_class]
    if not match.empty:
        description = match.iloc[0].get('Description', "No description available.")
        remedy = match.iloc[0].get('Remedy', "No remedy needed.")
        return description, remedy
    else:
        return "No description found.", "No remedy found."
