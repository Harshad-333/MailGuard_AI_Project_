
from pathlib import Path

import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "spam_assassin.csv"
MODEL_DIR = ROOT / "models"

# 1. Load and validate the dataset
if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

extra_path = ROOT / "data" / "legitimate_examples.csv"
if extra_path.exists():
    extra_df = pd.read_csv(extra_path)
    df = pd.concat([df, extra_df], ignore_index=True)

df = df.dropna(subset=["text", "label"]).copy()

df["text"] = df["text"].astype(str).str.strip()
df["label"] = (
    df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "ham": "Not Spam",
        "not spam": "Not Spam",
        "spam": "Spam",
    })
)

df = df[df["text"] != ""]
df = df[df["label"].isin(["Spam", "Not Spam"])]
df = df.drop_duplicates(subset=["text", "label"])

if df["label"].nunique() != 2:
    raise ValueError("Dataset must contain both Spam and Not Spam labels.")

if df["label"].value_counts().min() < 2:
    raise ValueError("Each class needs at least two examples.")

print("=" * 55)
print("EMAIL SPAM DETECTION - MODEL TRAINING")
print("=" * 55)
print(f"Usable emails: {len(df)}")
print("\nClass distribution:")
print(df["label"].value_counts().to_string())

# 2. Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.20,
    random_state=42,
    stratify=df["label"],
)

print(f"\nTraining emails: {len(X_train)}")
print(f"Testing emails:  {len(X_test)}")

# 3. Compare two machine learning algorithms
models = {
    "Naive Bayes": MultinomialNB(alpha=0.5),
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
    ),
}

results = []
trained_models = {}

for name, classifier in models.items():
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2),
                max_features=30000,
                sublinear_tf=True,
            ),
        ),
        ("classifier", classifier),
    ])

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test, predictions, pos_label="Spam", zero_division=0
    )
    recall = recall_score(
        y_test, predictions, pos_label="Spam", zero_division=0
    )
    f1 = f1_score(
        y_test, predictions, pos_label="Spam", zero_division=0
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Spam Precision": precision,
        "Spam Recall": recall,
        "Spam F1": f1,
    })

    trained_models[name] = pipeline

    print(f"\n{'-' * 55}")
    print(f"MODEL: {name}")
    print("-" * 55)
    print(f"Accuracy:       {accuracy:.3f}")
    print(f"Spam precision: {precision:.3f}")
    print(f"Spam recall:    {recall:.3f}")
    print(f"Spam F1-score:  {f1:.3f}")

    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        labels=["Not Spam", "Spam"],
        zero_division=0,
    ))

    print("Confusion matrix (rows = actual, columns = predicted):")
    print(confusion_matrix(
        y_test,
        predictions,
        labels=["Not Spam", "Spam"],
    ))

# 4. Compare models using spam F1-score
results_df = pd.DataFrame(results).sort_values(
    by="Spam F1", ascending=False
)

print("\n" + "=" * 55)
print("MODEL COMPARISON")
print("=" * 55)
print(results_df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

best_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_name]

# 5. Save the best model
MODEL_DIR.mkdir(exist_ok=True)
model_path = MODEL_DIR / "spam_classifier.joblib"
joblib.dump(best_model, model_path)

print(f"\nSelected model: {best_name}")
print(f"Saved model: {model_path}")
print("\nTraining and evaluation completed.")
print(
    "EVALUATION NOTE: The model was evaluated on a held-out "
    "test split of the SpamAssassin corpus. Results may differ "
    "on modern emails and other datasets. Further independent "
    "testing is recommended before real-world deployment."
)