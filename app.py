
import streamlit as st
import pandas as pd
import pickle
import base64

# Load trained model and label encoders
with open(r'predictive_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open(r"predictive_label.pkl", 'rb') as f:
    label_encoders = pickle.load(f)

# Define numerical and categorical column names
num_col = ['age', 'Year', 'Kilometers_Driven', 'Engine CC', 'Power', 'Seats', 'Mileage Km/L']
cat_cols = ['Manufacturer', 'Location', 'Fuel_Type', 'Transmission', 'Owner_Type']


def preprocess_and_predict_price(num_col, cat_cols, input_data, le, model, condition_rating, 
                                  traffic_violation, use_case, warranty, listing_duration, 
                                  vehicle_rating, vehicle_type):
    """
    Preprocesses input data and predicts car price using trained model.
    Adjusts the price based on various additional features.
    """
    # Preprocess numerical features
    num_data = input_data[num_col]
    num_data['age'] = 2023 - num_data['Year']

    # Preprocess categorical features
    cat_data = input_data[cat_cols].apply(lambda x: label_encoders[x.name].transform(x))
    cat_data = pd.DataFrame(cat_data, columns=cat_cols)

    # Combine processed data
    final_cols = ['Manufacturer', 'age', 'Year', 'Location', 'Kilometers_Driven', 
                  'Fuel_Type', 'Transmission', 'Owner_Type', 'Engine CC', 'Power', 
                  'Seats', 'Mileage Km/L']
    input_data_processed = pd.concat([cat_data, num_data], axis=1)
    input_data_processed = input_data_processed[final_cols]

    # Predict the base price
    predicted_price = model.predict(input_data_processed)[0]

    # Adjust price based on condition rating
    price_adjustment = condition_rating * 0.3 if predicted_price < 10 else condition_rating * 0.6
    predicted_price += price_adjustment

    # Adjust price for traffic violation
    if traffic_violation == "Yes":
        predicted_price *= 0.5

    # Adjust price for use case
    if use_case == "Commercial":
        predicted_price *= 2 / 3
    elif use_case == "Rental":
        predicted_price *= 3 / 4

    # Adjust price for warranty availability
    if warranty == "Yes":
        predicted_price *= 1.1  # Increase price by 10%

    # Adjust price for listing duration
    if listing_duration > 30:
        predicted_price *= 0.9  # Reduce by 10% for older listings

    # Adjust price for vehicle rating
    predicted_price += vehicle_rating * 0.2  # Add 20K per rating point

    # Adjust price for vehicle type
    if vehicle_type == "Luxury":
        predicted_price *= 1.5
    elif vehicle_type == "SUV":
        predicted_price *= 1.2

    return predicted_price

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        .star-dropdown, .traffic-dropdown, .usecase-dropdown {{
            width: 100%;
            max-width: 300px;
            margin: 0 auto;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
            color: #333;
            font-size: 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .star-dropdown:hover, .traffic-dropdown:hover, .usecase-dropdown:hover {{
            border-color: #ffcc00;
            background-color: #fff8e1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background image
add_bg_from_local(r"C:\Users\Virat Dwivedi\Pictures\download.jpeg")

# Define Streamlit UI
def main():
    st.title("Enhanced Used Car Price Prediction")
    st.write("Enter the car details below:")

    # Existing input fields
    year = st.number_input("Year of Manufacture", min_value=2000, max_value=2023, step=1)
    kilometers_driven = st.number_input("Kilometers Driven", min_value=0)
    engine_cc = st.number_input("Engine Displacement (CC)", min_value=0)
    power = st.number_input("Power (bhp)", min_value=0)
    seats = st.number_input("Number of Seats", min_value=0)
    mileage = st.number_input("Mileage (km/l)", min_value=0)

    manufacturer = st.selectbox("Manufacturer", label_encoders['Manufacturer'].classes_)
    location = st.selectbox("Location", label_encoders['Location'].classes_)
    fuel_type = st.selectbox("Fuel Type", label_encoders['Fuel_Type'].classes_)
    transmission = st.selectbox("Transmission", label_encoders['Transmission'].classes_)
    owner_type = st.selectbox("Owner Type", label_encoders['Owner_Type'].classes_)

    # New input fields
    warranty = st.selectbox("Warranty Availability", ["No", "Yes"])
    listing_duration = st.number_input("Listing Duration (in days)", min_value=0)
    vehicle_rating = st.slider("Vehicle Rating (1 to 5)", min_value=1, max_value=5, step=1)
    vehicle_type = st.selectbox("Type of Vehicle", ["Standard", "SUV", "Luxury"])
    traffic_violation = st.selectbox("Traffic Violation", ["No", "Yes"])
    use_case = st.selectbox("Use Case of Car", ["Personal", "Commercial", "Rental"])

    condition_rating = st.selectbox("Condition Rating", ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
    condition_rating = int(condition_rating.split()[0])

    # Create input data DataFrame
    input_data = pd.DataFrame({
        'Manufacturer': [manufacturer],
        'age': [2023 - year],
        'Year': [year],
        'Location': [location],
        'Kilometers_Driven': [kilometers_driven],
        'Fuel_Type': [fuel_type],
        'Transmission': [transmission],
        'Owner_Type': [owner_type],
        'Engine CC': [engine_cc],
        'Power': [power],
        'Seats': [seats],
        'Mileage Km/L': [mileage]
    })

    # Predict car price
    predicted_price = preprocess_and_predict_price(num_col, cat_cols, input_data, label_encoders, model,
                                                   condition_rating, traffic_violation, use_case,
                                                   warranty, listing_duration, vehicle_rating, vehicle_type)

    # Display predicted price
    st.write("Predicted Car Price (in lakhs):", round(predicted_price, 2))


if __name__ == '__main__':
    main()
