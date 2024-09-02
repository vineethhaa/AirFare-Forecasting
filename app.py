import streamlit as st
import pickle
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt

# Load the machine learning model
path = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(path, 'c1_flight_gbr.pkl'))

# Streamlit UI
st.set_page_config(page_title="Flight Price Prediction")

# Navigation
page = st.sidebar.selectbox("Select a page", ["Home"])

if page == "Home":
    st.title("Flight Price Prediction")
    st.write("Welcome to the Flight Price Prediction app!")

    # Input form
    st.header("Enter Flight Details")

    # Date of Departure
    departure_date = st.date_input("Date of Departure", min_value=None, max_value=None)

    departure_time = st.time_input("Time of Departure")

    # Date of Arrival
    arrival_date = st.date_input("Date of Arrival", min_value=None, max_value=None)

    arrival_time = st.time_input("Time of Arrival")

    # Source and Destination
    source = st.selectbox("Travelling from (Source)", ["Delhi", "Kolkata", "Mumbai", "Chennai"])
    destination = st.selectbox("Travelling To (Destination)", ["Cochin", "Delhi", "Hyderabad", "Kolkata"])

    # Number of Stops
    stops = st.selectbox("No. of Stops", ["0", "1", "2", "3", "4"])

    # Preferred Airline
    airline = st.selectbox(
        "Preferred Airline",
        [
            "Jet Airways", "IndiGo", "Air India", "Multiple carriers", "SpiceJet", "Vistara", "Air Asia", "GoAir",
            "Multiple carriers Premium economy", "Jet Airways Business", "Vistara Premium economy", "Trujet"
        ]
    )

    # Predict Button
    if st.button("Predict Price"):
        # Convert datetime to features
        journey_day = departure_date.day
        journey_month = departure_date.month
        dep_hour = departure_time.hour
        dep_min = departure_time.minute
        arrival_hour = arrival_time.hour
        arrival_min = arrival_time.minute
        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)

        # Encode airline, source, and destination
        airlines = {
            'Jet Airways': 0, 'IndiGo': 1, 'Air India': 2, 'Multiple carriers': 3, 'SpiceJet': 4, 'Vistara': 5,
            'Air Asia': 6, 'GoAir': 7, 'Multiple carriers Premium economy': 8, 'Jet Airways Business': 9,
            'Vistara Premium economy': 10, 'Trujet': 11
        }
        Airline_encoded = [0] * 12
        Airline_encoded[airlines[airline]] = 1

        sources = {'Delhi': 0, 'Kolkata': 1, 'Mumbai': 2, 'Chennai': 3}
        Source_encoded = [0] * 4
        Source_encoded[sources[source]] = 1

        destinations = {'Cochin': 0, 'Delhi': 1, 'Hyderabad': 2, 'Kolkata': 3}
        Destination_encoded = [0] * 4
        Destination_encoded[destinations[destination]] = 1

        # Create a DataFrame with the input features
        input_data = pd.DataFrame(
            [[stops, journey_day, journey_month, dep_hour, dep_min, arrival_hour, arrival_min, Duration_hour,
              Duration_mins] + Airline_encoded + Source_encoded + Destination_encoded],
            columns=['Total_Stops', 'Journey_Day', 'Journey_Month', 'Dep_Hour', 'Dep_Min', 'Arrival_Hour',
                     'Arrival_Min', 'Duration_Hours', 'Duration_Mins'] +
                    [f'Airline_{i}' for i in range(12)] +
                    [f'Source_{i}' for i in range(4)] +
                    [f'Destination_{i}' for i in range(4)]
        )

        # Predict flight price
        expected_num_features = 24  # Replace with the actual number of features in your model
        input_data = input_data.iloc[:, :expected_num_features]
        prediction = model.predict(input_data)
        output = round(prediction[0], 2)

        st.write(f"Your Flight price is Rs. {output}")