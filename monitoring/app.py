import streamlit as st
import json
import matplotlib.pyplot as plt
import os
import pandas as pd

# title and description
st.title('Movie Review Sentiment Monitoring App')
st.markdown("This app will be used to monitor the backend FastAPI application by plotting different data to help in analysing model performance.")

# cache data sources
@st.cache_data
def load_data():
    df = pd.read_csv("IMDB Dataset.csv")
    df["sentence_length"] = df["review"].astype(str).apply(lambda x: len(x.split()))
    return df

@st.cache_data
def load_logs():
    if not os.path.exists("/logs/prediction_logs.json"):
        print("no log file")
        return pd.DataFrame(columns=["sentence_length"])
    
    with open("/logs/prediction_logs.json", "r") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    df = pd.DataFrame(lines)
    if "request_text" in df.columns:
        df["sentence_length"] = df["request_text"].astype(str).apply(lambda x: len(x.split()))
    else:
        df["sentence_length"] = []
    return df

imdb_df = load_data()
log_df = load_logs()

# Data Drift Analysis: Create a histogram or density plot comparing the distribution of sentence lengths from your IMDB Dataset.csv against the lengths from the logged inference requests. 
st.subheader("Histogram of Sentence Lengths")

plt.figure(figsize=(10, 5))
plt.hist(imdb_df["sentence_length"], bins=50, alpha=0.5, label="IMDB Dataset")
plt.hist(log_df["sentence_length"], bins=50, alpha=0.5, label="Inference Logs")
plt.legend()
plt.xlabel("Sentence Length (word count)")
plt.ylabel("Frequency")
plt.title("Sentence Length Distribution Comparison")
st.pyplot(plt)

# Target Drift Analysis: Create a bar chart showing the distribution of predicted sentiments from the logs vs trained sentiments

# Model Accuracy & User Feedback: From the true_sentiment logged in the logs
# Calculate and display the model's accuracy and precision based on all collected feedback.
# Implement Alerting: If the calculated accuracy drops below 80%, display a prominent warning banner at the top of the dashboard using st.error().