#!/usr/bin/env python
import os
import pandas as pd
from transformers import pipeline


def main():
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    input_path = "data.csv"
    output_path = "submission.csv"

    df = pd.read_csv(input_path)

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="model"
    )

    texts = df["MessageText"].tolist()
    predictions = sentiment_pipeline(texts, truncation=True)

    mapping = {
        "LABEL_0": "neutral",
        "LABEL_1": "positive",
        "LABEL_2": "negative"
    }
    letter_preds = [mapping.get(pred["label"], pred["label"]) for pred in predictions]

    submission = pd.DataFrame({
        "UserSenderId": df["UserSenderId"],
        "Class": letter_preds
    })

    submission.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
