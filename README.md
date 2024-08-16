# ProEvento
ProEvento is an AI-driven event planner, orchestrating seamless events through personalized recommendations and real-time data analysis.  Its intuitive interface and collaborative features streamline planning, ensuring memorable experiences for both organizers and attendees.

## Features

- **User Authentication:** Secure sign-up and login functionality.
- **Event Creation:** Users can create events by providing details such as event name, location, date, space capacity, budget, and a description.
- **Venue Recommendation:** The app uses machine learning to recommend venues that best match the event details provided by the user.
- **Booking Management:** Users can check the availability of venues and book them directly through the app.
- **Event Calendar:** Users can view and manage their scheduled events in a calendar view.

## Tech Stack

- **Python**: Used for backend development and machine learning.
- **Flask**: A micro web framework used to build RESTful APIs and serve HTML pages.
- **Streamlit**: A Python library used to create the interactive front-end of the application.
- **MongoDB**: NoSQL database used to store user and event details.
- **Pandas**: Used for data manipulation and preprocessing.
- **scikit-learn**: Utilized for implementing machine learning models.
- **Sentence Transformers**: Used to encode text data into embeddings for similarity comparison.
- **Jupyter Notebook**: Used for model development and testing.
- **HTML/CSS/JavaScript**: Frontend technologies used for creating responsive web pages.

## Machine Learning Models

### 1. **Sentence Transformer Model**
- **Model**: `distiluse-base-multilingual-cased`
- **Purpose**: To encode event and venue details into vector representations.
- **Application**: These vectors are used to calculate cosine similarities between the user input and venue details to provide relevant recommendations.

### 2. **Cosine Similarity**
- **Purpose**: To measure the similarity between user preferences and venue details.
- **Application**: The cosine similarity scores are used to rank and recommend venues to users.

## API Endpoints

- **/recommend** (POST): Takes event details as input and returns a list of recommended venues.
- **/signup** (POST): Registers a new user.
- **/login** (POST): Logs in an existing user.
- **/events** (GET): Fetches events created by the logged-in user.
- **/book** (POST): Books a venue for the event.
- **/calendar** (GET): Displays the user's events in a calendar view.

## Installation and Setup

### 1. Clone the Repository:
```bash
git clone https://github.com/your-username/ai-event-planner.git
cd ai-event-planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Run the Flask Backend

```bash
python flask_bk.py
```
### 4. Run the Streamlit Frontend

```bash
streamlit run create_event_st1.ipynb
```
### Project Structure
```plaintext

ai-event-planner/
│
├── templates/                  # HTML templates for the Flask app
│   ├── signup.html
│   ├── login.html
│   ├── homepage.html
│   ├── calendar.html
│   ├── recommendations.html
│   ├── user_events.html
│   ├── welcome.html
├── static/                     # Static files (CSS, JS, images)
│   ├── styles.css
│   ├── script.js
├── flask_bk.py                      # Main Flask application
├── create_event_st1.ipynb               # Streamlit application code
├── requirements.txt            # List of dependencies
├── README.md                   # Project documentation
└── data/                       # Data files for model and recommendations
    ├── modified_user_data1.csv
    ├── handled_venues.csv
```
### Usage
Create an Event: After logging in, navigate to the 'Create Event' page where you can enter the details of your event.
Get Recommendations: Once the event details are submitted, click on "Get Recommendations" to receive venue suggestions.
Book a Venue: If you find a suitable venue, you can book it directly through the app.
Manage Events: View your events and their details in the 'User Events' section or in the calendar.
