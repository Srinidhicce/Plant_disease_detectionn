import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load model
model_path = 'C:/Users/Administrator/Desktop/active/Leave_detection/Plant/best_leaf.h5'
model = load_model(model_path)

# Load the new remedies CSV (disease_info.csv)
remedies_df = pd.read_csv('C:/Users/Administrator/Desktop/active/Leave_detection/Plant/disease_info.csv')

# Strip whitespaces from headers
remedies_df.columns = [col.strip() for col in remedies_df.columns]

# Final class names (based on folder structure)
class_names = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy"
]


def get_leaf_result(file_path):
    try:
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        confidence = float(prediction[0][predicted_index])
        predicted_class = class_names[predicted_index]

        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence: {confidence}")

        return predicted_class, confidence
    except Exception as e:
        print(f"Error while processing the image: {e}")
        return None, 0


def get_leaf_remedy_info(predicted_class):
    try:
        # Normalize class name for search
        predicted_class_normalized = predicted_class.strip().lower()
        remedies_df['Folder Name'] = remedies_df['Folder Name'].astype(str).str.lower()

        # Try to match disease name from the class name to disease mapping
        match_row = remedies_df[
            remedies_df['Folder Name'].str.contains(predicted_class_normalized.split("_")[0], case=False)]

        if not match_row.empty:
            disease = match_row.iloc[0]["Disease Name"]
            remedy = match_row.iloc[0]["Organic Cure Suggestion"]
            print(f"Disease: {disease}")
            print(f"Remedy: {remedy}")
        else:
            disease = "No description found"
            remedy = "No remedy found"
            print("No matching disease found in the remedies file.")

        return disease, remedy
    except Exception as e:
        print(f"Error while fetching disease information: {e}")
        return "Unknown Disease", "No Remedy Available"


# Example usage
image_path = 'C:/path/to/your/image.jpg'  # Replace with your image path
predicted_class, confidence = get_leaf_result(image_path)

if predicted_class:
    disease, remedy = get_leaf_remedy_info(predicted_class)
