#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import plotly.graph_objects as go
import joblib
import plotly.express as px

st.set_page_config(layout="wide")


@st.cache_data
def load_data_and_defaults():
    """
    Load the dataset, preprocess it, and compute default values for model features.
    """
    # Load the dataset
    file_path = "D:/MSDA_SJSU/Data 230/Project/eda_data_v0.1.csv"
    df = pd.read_csv(file_path)

    # Ensure 'host_is_superhost' is one-hot encoded
    if 'host_is_superhost' in df.columns:
        df = pd.get_dummies(df, columns=['host_is_superhost'], prefix='host_is_superhost', drop_first=False)

    # Define the required model features
    model_features = [
        'host_listings_count', 'host_total_listings_count', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'price',
        'minimum_nights', 'minimum_minimum_nights', 'maximum_minimum_nights', 'minimum_maximum_nights',
        'maximum_maximum_nights', 'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm', 'availability_30', 
        'availability_60', 'availability_90', 'availability_365', 'number_of_reviews', 'number_of_reviews_ltm',
        'number_of_reviews_l30d', 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication', 'review_scores_location', 'review_scores_value',
        'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes', 'reviews_per_month',
        'year_round_occupancy_rate', 'month_round_occupancy_rate', 
  #      'revenue_per_rental', 'monthly_revenue_per_rental',
        'host_is_superhost_Not Superhost', 'host_is_superhost_Superhost'
    ]

    # Check for missing features in the dataset
    missing_features = [feature for feature in model_features if feature not in df.columns]
    if missing_features:
        st.error(f"The following required features are missing in the dataset: {missing_features}")
        st.stop()

    # Compute default median values for the specified features
    default_values = df[model_features].median().to_dict()

    return df, default_values, model_features

@st.cache_resource
def load_model_and_scaler():
    """
    Load the pre-trained scaler and KMeans model from pickle files.
    """
    # Load the pre-trained scaler
    scaler_data = joblib.load("scaler.pkl")
    if isinstance(scaler_data, dict):
        scaler = scaler_data.get("scaler")  # Extract the scaler object
        if scaler is None:
            raise ValueError("The 'scaler.pkl' file does not contain a valid scaler.")
    else:
        scaler = scaler_data  # Assume scaler_data is the scaler itself

    # Load the pre-trained KMeans model
    kmeans = joblib.load("kmeans.pkl")
    if not isinstance(kmeans, KMeans):
        raise ValueError("The 'kmeans.pkl' file does not contain a valid KMeans model.")

    return scaler, kmeans


# Load data, defaults, and models
df, DEFAULT_FEATURE_VALUES, FEATURES = load_data_and_defaults()
scaler, kmeans = load_model_and_scaler()

# Sidebar navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Select what you want to display:",
    ["Home", "Data Snippet", "Scatter Plot", "Rental Description Wordcloud", "Predict Rank and Revenue"]
)


def home():
    st.title("Welcome to the Rental Cluster Model App")
    st.write("This app predicts the rank and average monthly revenue of rentals based on user inputs.")
    st.write("Use the sidebar to navigate between prediction functionality and dataset exploration.")


def data_snippet():
    st.header("Data Snippet")
    st.write(df.head())


def scatter_plot():
    st.header("Scatter Plot")

    # Filter numeric columns
    numeric_columns = df.select_dtypes(include=["number"]).columns

    # Dropdown menus for X and Y axes
    col1, col2 = st.columns(2)
    x_axis_val = col1.selectbox("Select the X-axis", options=numeric_columns)
    y_axis_val = col2.selectbox("Select the Y-axis", options=numeric_columns)

    # Scatter plot with hue
    plot = px.scatter(
        df,
        x=x_axis_val,
        y=y_axis_val,
        color=df["host_is_superhost_Superhost"],  # Use Superhost as hue
        title=f"Scatter Plot of {x_axis_val} vs {y_axis_val} (Colored by Host Status)",
        labels={"host_is_superhost_Superhost": "Host Status"}
    )
    st.plotly_chart(plot, use_container_width=True)


def rental_description_wordcloud():
    st.header("Rental Description Wordcloud")

    # Interactive city selection
    city_list = df["City"].dropna().unique()
    selected_city = st.selectbox("Select a City", city_list)

    if selected_city:
        city_data = df[df["City"] == selected_city]

        if city_data["description"].notnull().any():
            text = " ".join(description for description in city_data["description"].dropna())

            # Generate wordcloud
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig = go.Figure(go.Image(z=wordcloud.to_array()))

            fig.update_layout(
                title=f"Hosts' Favorite Rental Description Words for {selected_city}",
                xaxis_showgrid=False, yaxis_showgrid=False,
                xaxis_zeroline=False, yaxis_zeroline=False,
                xaxis_showticklabels=False, yaxis_showticklabels=False,
                height=500,
            )
            st.plotly_chart(fig)
        else:
            st.error(f"No descriptions available for rentals in {selected_city}.")


def predict_rank_and_revenue():
    st.title("Predict Rental Rank and Revenue")
    st.write("Provide input values to predict the rank of the rental and the corresponding average monthly revenue.")

    # Dropdown filters for State and City
    state_list = df["State"].dropna().unique()
    selected_state = st.selectbox("Select a State", state_list)
    filtered_cities = df[df["State"] == selected_state]["City"].dropna().unique()
    selected_city = st.selectbox("Select a City", filtered_cities)

    # Filter the dataset based on State and City
    filtered_data = df[(df["State"] == selected_state) & (df["City"] == selected_city)].copy()  # Use .copy() to avoid warnings
    if filtered_data.empty:
        st.error("No data available for the selected State and City. Please try another selection.")
        return

    # Add predicted cluster labels to filtered_data
    try:
        filtered_data_scaled = scaler.transform(filtered_data[FEATURES])
        filtered_data["Cluster"] = kmeans.predict(filtered_data_scaled)
    except Exception as e:
        st.error(f"Error during clustering for filtered data: {e}")
        return

    # User input form
    st.write("**Provide the features for your rental!**")
    user_inputs = {}

    for feature in [
        "bedrooms", "bathrooms", "accommodates", "price", "minimum_nights"
    ]:
        if feature == "price":
            user_inputs[feature] = st.number_input(
                f"Enter value for {feature.replace('_', ' ').capitalize()}:",
                min_value=10,
                max_value=5000,
                step=10,
                value=int(DEFAULT_FEATURE_VALUES.get(feature, 100)),  # Default value for price
            )
        else:
            user_inputs[feature] = st.number_input(
                f"Enter value for {feature.replace('_', ' ').capitalize()}:",
                min_value=0,
                max_value=100,
                step=1,
                value=int(DEFAULT_FEATURE_VALUES.get(feature, 0)),
            )

    # Initialize user input DataFrame
    user_input = pd.DataFrame([user_inputs])

    # Fill in missing features with default (median) values
    missing_features = [feature for feature in FEATURES if feature not in user_input.columns]
    for feature in missing_features:
        user_input[feature] = DEFAULT_FEATURE_VALUES.get(feature, 0)

    # Ensure user_input matches model features
    user_input = user_input[FEATURES]

    if st.button("**Predict Revenue**"):
        try:
            # Scale the input
            user_input_scaled = scaler.transform(user_input)

            # Predict cluster
            predicted_cluster = kmeans.predict(user_input_scaled)[0]

            # Compute cluster ranking
            cluster_revenue_ranking = (
                filtered_data.groupby("Cluster")["monthly_revenue_per_rental"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )
            cluster_revenue_ranking["Rank"] = cluster_revenue_ranking["monthly_revenue_per_rental"].rank(
                ascending=False
            )

            if predicted_cluster not in cluster_revenue_ranking["Cluster"].values:
                st.error(f"Predicted cluster {predicted_cluster} not found.")
                return

            # Get rank and revenue for the predicted cluster
            rank = cluster_revenue_ranking.loc[
                cluster_revenue_ranking["Cluster"] == predicted_cluster, "Rank"
            ].values[0]
            avg_revenue = cluster_revenue_ranking.loc[
                cluster_revenue_ranking["Cluster"] == predicted_cluster, "monthly_revenue_per_rental"
            ].values[0]

            # Display results
            st.write(f"**Predicted Cluster Rank:** {int(rank)}")
            st.write(f"**Average Monthly Revenue for the Cluster:** ${avg_revenue:,.2f}")
            st.subheader("Cluster Ranking Table")
            st.write(cluster_revenue_ranking)

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")


if options == "Home":
    home()
elif options == "Data Snippet":
    data_snippet()
elif options == "Scatter Plot":
    scatter_plot()
elif options == "Rental Description Wordcloud":
    rental_description_wordcloud()
elif options == "Predict Rank and Revenue":
    predict_rank_and_revenue()
