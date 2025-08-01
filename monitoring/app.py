import streamlit as st
import json

# title and description
st.title('Movie Review Sentiment Monitoring App')
st.markdown("This app will be used to monitor the backend FastAPI application by plotting different data to help in analysing model performance.")

# Data Drift Analysis: Create a histogram or density plot comparing the distribution of sentence lengths from your IMDB Dataset.csv against the lengths from the logged inference requests. 

# Target Drift Analysis: Create a bar chart showing the distribution of predicted sentiments from the logs vs trained sentiments

# Model Accuracy & User Feedback: From the true_sentiment logged in the logs
# Calculate and display the model's accuracy and precision based on all collected feedback.
# Implement Alerting: If the calculated accuracy drops below 80%, display a prominent warning banner at the top of the dashboard using st.error().