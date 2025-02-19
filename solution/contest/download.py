#!/usr/bin/env python
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def main():
    model_name = "Megnis/rubert-tiny2-sentiment-analisys-RuSentimentUnion-9000-2"
    target_dir = "C:/Рабочий стол/Hackatons/Sentiment-analisis-system/solution/contest/model"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"Downloading model '{model_name}' to '{target_dir}'...")

    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model.save_pretrained(target_dir)
    tokenizer.save_pretrained(target_dir)

    print("Model download completed.")


if __name__ == "__main__":
    main()
