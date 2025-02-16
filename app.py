import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pandas as pd
from transformers import pipeline
from config import MODELS, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, LABEL_MAPPING

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def precache_models_with_pipeline():
    """
    Для каждой модели из конфигурации создаём объект pipeline,
    что приводит к загрузке всех файлов модели в указанный каталог кэша.
    После этого объект удаляется, чтобы не занимать оперативную память.
    """
    for model_name, model_id in MODELS.items():
        try:
            print(f"Pre-caching model '{model_name}' using pipeline...")
            pipe = pipeline("sentiment-analysis", model=model_id, cache_dir=None)
            pipe("This is a dummy sentence for caching purposes.")
            del pipe
            print(f"Model '{model_name}' cached on disk.")
        except Exception as e:
            print(f"Error caching model '{model_name}': {e}")


precache_models_with_pipeline()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_model = request.form.get("model")
        file = request.files.get("file")
        comment_column = request.form.get("comment_column")

        if not selected_model or selected_model not in MODELS:
            flash("Выберите корректную модель.")
            return redirect(request.url)
        if not file or file.filename == "":
            flash("Выберите файл для загрузки.")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Допустимые форматы: csv, xlsx.")
            return redirect(request.url)
        if not comment_column:
            flash("Выберите столбец с комментариями.")
            return redirect(request.url)

        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_id + "." + file_ext)
        file.save(file_path)

        try:
            if file_ext == "csv":
                df = pd.read_csv(file_path)
            elif file_ext == "xlsx":
                df = pd.read_excel(file_path)
        except Exception as e:
            flash("Ошибка при чтении файла: " + str(e))
            return redirect(request.url)

        if comment_column not in df.columns:
            flash("Выбранный столбец с комментариями не найден в файле.")
            return redirect(request.url)

        model_id = MODELS[selected_model]
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_id)

        texts = df[comment_column].astype(str).tolist()
        predictions = sentiment_pipeline(texts, truncation=True)

        pred_labels = [LABEL_MAPPING.get(pred["label"], pred["label"]) for pred in predictions]
        df["prediction"] = pred_labels

        result_filename = unique_id + "_predictions.csv"
        result_path = os.path.join(app.config["UPLOAD_FOLDER"], result_filename)
        df.to_csv(result_path, index=False)

        distribution = df["prediction"].value_counts(normalize=True).mul(100).round(2).to_dict()

        table_html = df.to_html(classes="table table-striped", index=False)

        return render_template(
            "results.html",
            table_html=table_html,
            distribution=distribution,
            download_filename=result_filename
        )
    return render_template("index.html", models=MODELS)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
