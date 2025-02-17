MODELS = {
    "RuBERT-tiny2-best": "Megnis/rubert-tiny2-sentiment-analisys-RuSentimentUnion-9000-2",
    "RuBERT-tiny": "Megnis/rubert-tiny-sentiment-analisys",
    "DistilBERT": "Megnis/distilbert-base-multilingual-cased-sentiment-analisys"
}

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx"}

LABEL_MAPPING = {
    "LABEL_0": "neutral",
    "LABEL_1": "positive",
    "LABEL_2": "negative"
}