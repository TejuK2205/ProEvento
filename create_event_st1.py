import streamlit as st
import requests

login_bg_color = """
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://i.pinimg.com/originals/22/56/b2/2256b240528fe695ef7915ef96498152.jpg")

    }
[class^=st-emotion] {
    font-family: 'Roboto';
    color: black;
    font-weight: bold;
    font-size: 30px;
}
[class^=".st-emotion-cache-"] {
    word-break: break-word;
    margin-bottom: 0px;
    font-size: 20px;
}

</style>
"""

def create_event():
    # Add background image
    st.markdown(login_bg_color, unsafe_allow_html=True)

    st.title("Create Event")

    # Event details form
    st.subheader("Event Details")
    event_name = st.text_input("Event Name")
    location = st.text_input("Location")
    date = st.date_input("Date")
    space_capacity = st.number_input("Space Capacity", min_value=1)
    budget = st.number_input("Budget", min_value=0)
    description = st.text_area("Description")

    if st.button("Get Recommendations"):
        # Make a call to your Flask API to get recommendations
    
        payload = {
            "eventName": event_name,
            "location": location,
            "date": str(date),
            "spaceCapacity": space_capacity,
            "budget": budget,
            "description": description
        }
        response = requests.post("http://127.0.0.1:5000/recommend", json=payload)

        if response.status_code == 200:
            recommendations = response.json()
            # Display recommendations
            st.subheader("Recommendations")
            for venue in recommendations:
                st.write(f"Venue: {venue['Venue Name']}")
                st.write(f"Location: {venue['Location']}")
                st.write(f"Overview: {venue['Overview']}")
                st.write(f"Rating: {venue['Rating']}")
                st.write(f"Reviews: {venue['Reviews']}")
                st.write("-" * 50)
        else:
            st.error("Failed to fetch recommendations. Please try again later.")

create_event()