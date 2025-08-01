import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# create app
app = FastAPI(
    title="Movie Review Sentiment Analysis",
)

# load model
try:
    model = joblib.load("sentiment_model.pkl")
except FileNotFoundError:
    print("Model file not found")
    model = None

# create prediction request model
class PredictionRequest(BaseModel):
    text: str

# generate startup event
@app.on_event("startup")
def startup_event():
    """
    Startup event to print if model is loaded or not
    """
    if model is None:
        print("Warning: Model not loaded")
    else:
        print("Model loaded successfully")

# get health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify if the API is running
    """
    if model is None:
        return {"status": "unhealthy", "message": "Model not loaded but app is running"}
    return {"status": "healthy", "message": "Model loaded successfully and app is running"}

# create predict endpoint
@app.post("/predict")
def predict(request: PredictionRequest):
    """
    Predict endpoint to predict the sentiment of the provided review text.
    Returns a JSON object with the predicted sentiment, "positive" or "negative"
    """
    # check if model is loaded  
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded")
    
    # predict sentiment
    try:
        prediction = model.predict([request.text])
        return {"sentiment": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error predicting sentiment: {e}")

# create predict probability endpoint
@app.post("/predict_proba")
def predict_with_probabilities(request: PredictionRequest):
    """
    Predict probability endpoint to predict the probability of the sentiment of the provided review text.
    Returns a JSON object with the predicted probability of the sentiment, and the predicted sentiment, "positive" or "negative"
    """
    # check if model is loaded
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded")

    # predict sentiment with probabilities
    try:
        probabilities = model.predict_proba([request.text])
        prediction = model.predict([request.text])
        prob = probabilities[0][0] if prediction[0] == "negative" else probabilities[0][1]
        return {"sentiment": prediction[0], "probability": prob}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error predicting sentiment: {e}")
        
# get training example endpoint
@app.get("/example")
def example():
    """
    Training example endpoint to return a training example from the dataset
    Returns a JSON object with the text of a random review from the IMDB csv file
    """
    try:
        # Read the CSV file
        df = pd.read_csv("IMDB Dataset.csv")
        
        # Get a random row
        random_row = df.sample(n=1).iloc[0]
        
        return {
            "review": random_row["review"]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error reading CSV file: {e}")