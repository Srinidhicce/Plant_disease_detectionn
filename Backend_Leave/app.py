from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
import os

from plant_detector import get_result, get_remedy_info
from chat_handler import get_chat_response
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Dummy DB
users = {}
chat_histories = {}


# MongoDB setup
client = MongoClient("mongodb://localhost:27017/Plant_Chat")  # or your Atlas URL
db = client.chatbotDB
chat_collection = db.chats

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from leaf_detector import get_leaf_result, get_leaf_remedy_info
@app.route('/api/leaf-predict', methods=['POST'])
def api_leaf_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded file with a unique filename
    filename = secure_filename(f"{uuid.uuid4().hex}_{f.filename}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(file_path)

    # Predict class and confidence using the uploaded image
    predicted_class, confidence = get_leaf_result(file_path)

    # Get the disease and remedy from the prediction
    disease, remedy = get_leaf_remedy_info(predicted_class)

    # Return the result with the correct image URL
    return jsonify({
        'prediction': predicted_class,
        'confidence': f"{confidence * 100:.2f}%",
        'disease': disease,
        'remedy': remedy,
        'imageUrl': f'/static/uploads/{filename}'
    })

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(f"{uuid.uuid4().hex}_{f.filename}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(file_path)

    predicted_class, confidence = get_result(file_path)
    description, remedy = get_remedy_info(predicted_class)

    return jsonify({
        'prediction': predicted_class,
        'confidence': f"{confidence * 100:.2f}%",
        'description': description,
        'remedy': remedy,
        'imageUrl': f'/static/uploads/{filename}'
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    session_id = data.get("session_id")
    message = data.get("message")

    if not session_id or not message:
        return jsonify({'error': 'Missing session_id or message'}), 400

    # Get response (you already have this logic)
    response = get_chat_response(message)

    # Save both user and bot message
    chat_collection.insert_many([
        {"session_id": session_id, "sender": "user", "message": message, "timestamp": datetime.utcnow()},
        {"session_id": session_id, "sender": "bot", "message": response, "timestamp": datetime.utcnow()},
    ])

    return jsonify({"response": response})

@app.route('/api/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    messages = list(chat_collection.find({"session_id": session_id}, {"_id": 0}))
    return jsonify({"chat_history": messages})


#signup deatils
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input fields
    if not username or not email or not password:
        return jsonify({"msg": "Missing username, email, or password"}), 400

    # Validate email format
    try:
        valid = validate_email(email, check_deliverability=False)
        email = valid.email  # Normalized email
    except EmailNotValidError as e:
        return jsonify({"msg": str(e)}), 400

    # Check if username or email already exists
    if username in users:
        return jsonify({"msg": "Username already exists"}), 409
    if any(user['email'] == email for user in users.values()):
        return jsonify({"msg": "Email already registered"}), 409

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Store user information
    users[username] = {
        'email': email,
        'password': hashed_password
    }
    chat_histories[username] = []

    return jsonify({"msg": "User registered successfully"}), 201


#login deatils
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if username not in users or not bcrypt.check_password_hash(users[username], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify(access_token=token), 200

if __name__ == '__main__':
    app.run(debug=True)
