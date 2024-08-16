from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np

app = Flask(__name__)
app.template_folder = 'C:\\Users\\ADMIN\\OneDrive\\Desktop\\AI&DS\\TNcpl041\\project\\app\\templates'

client = MongoClient('mongodb://localhost:27017/')
db = client.event_planner
users_collection = db.user_info
event_details_collection = db.event_details 
collection = db['event_details']

app.config['DEBUG'] = True

user_interactions_data = pd.read_csv("C:/Users/ADMIN/OneDrive/Desktop/AI&DS/TNcpl041/modified_user_data1.csv")

venue_details_data = pd.read_csv("C:/Users/ADMIN/OneDrive/Desktop/AI&DS/TNcpl041/handled_venues.csv")

model = SentenceTransformer("distiluse-base-multilingual-cased")

venue_data = pd.read_csv("C:/Users/ADMIN/OneDrive/Desktop/AI&DS/TNcpl041/handled_venues.csv")  # Replace with your actual path

venue_data['combined_text'] = venue_data[['Venue Name', 'Location', 'Overview', 'Ambience', 'Services Offered', 'Facilities', 'USPs', 'Decoration Policy', 'Catering Policy']].fillna('').agg(' '.join, axis=1)

# Encode the combined text using the pre-trained model
venue_embeddings = model.encode(venue_data['combined_text'].tolist())

def recommend_venues(user_data, top_n=5, min_similarity=0.5):
    user_text = ' '.join([str(value) for key, value in user_data.items() if key != 'user_id'])
    user_embedding = model.encode([user_text])  # Notice the square brackets to make it a list
    similarities = cosine_similarity(user_embedding, venue_embeddings)

    similar_indices = (similarities >= min_similarity).flatten()
    similar_venues = venue_data[similar_indices]

    if len(similar_venues) == 0:
        top_indices = similarities.argsort()[0][-top_n:][::-1]
        recommended_venues = venue_data.iloc[top_indices]

    else:
        top_indices = similarities.argsort()[0][-top_n:][::-1]
        recommended_venues = similar_venues.iloc[top_indices]
    
    # Filter out only specific columns
    recommended_venues_filtered = recommended_venues[["Venue Name", "Location", "Overview", "Rating", "Reviews"]]
    return recommended_venues_filtered.to_dict(orient='records')  # Convert DataFrame to list of dictionaries

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    user_data = request.get_json()
    recommended_venues = recommend_venues(user_data)
    return jsonify(recommended_venues)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route("/create_event_")
def create():
    return redirect("http://localhost:8502")

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/user_events')
def user_events():
    return render_template('user_events.html')

@app.route('/view_event')
def view_event():
    return render_template('user_events.html')


@app.route("/signup", methods=["POST"])
def signup():
    user_data = request.json
    username = user_data.get("username")
    password = user_data.get("password")
    email = user_data.get("email")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Username already exists"}), 400

    users_collection.insert_one({
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    })

    return jsonify({"message": "User created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")

    user = users_collection.find_one({"username": username})

    if user and user["password"] == password:
        user_id = user.get("user_id")
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
    

@app.route("/events", methods=["GET"])
def get_user_events():
    user_id = request.args.get('user_id')

    user_events = list(event_details_collection.find({"user_id": user_id}, {"_id": 0, "events": 1}))

    return jsonify(user_events)

@app.route("/calendar")
def calendar():
    events = list(event_details_collection.find({}, {"_id": 0, "date": 1, "event_name": 1}))

    return render_template("calendar.html", events=events)


@app.route('/book', methods=['POST'])
def book():
    booking_data = request.form.to_dict()

    user_id = booking_data.get("user_id")
    event_name = booking_data.get("event_name")
    location = booking_data.get("location")
    date = booking_data.get("date")
    space_capacity = booking_data.get("space_capacity")
    budget = booking_data.get("budget")
    description = booking_data.get("description")

    available = check_availability(location, date)
    
    if available:
        booking = {
            "user_id": user_id,
            "event_name": event_name,
            "location": location,
            "date": date,
            "space_capacity": space_capacity,
            "budget": budget,
            "description": description
        }
        collection.insert_one(recommended_venues[1])
        return jsonify({'message': 'Venue booked successfully!'})
    else:
        return jsonify({'error': 'Venue not available on the selected date!'})

def check_availability(location, date):
    booking = collection.find_one({'location': location, 'date': date})
    if booking:
        return False
    else:
        return True


if __name__ == "__main__":
    app.run(debug=True)
