# models.py

from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

def train_svd_model(event_history_df):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(event_history_df[["UserId", "EventId", "Rate"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    model = SVD()
    model.fit(trainset)
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    return model, predictions, rmse
