# AI-Powered Email Spam Detection System

## Included features
- Python + scikit-learn text classification using TF-IDF and Multinomial Naive Bayes.
- Streamlit web interface for pasting an email.
- Optional Gemini API integration to generate a plain-language explanation.
- Built-in explanation fallback when there is no API key or the API is unavailable.
- Training script that prints holdout accuracy, precision, recall and F1-score.

## Run on Windows
1. Extract this ZIP into a folder.
2. Double-click `run_windows.bat`, or open PowerShell in this folder and run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   py train_model.py
   py -m streamlit run app.py
   ```
3. Open the local URL printed in the terminal, usually `http://localhost:8501`.

If PowerShell blocks activation, run `py -m pip install -r requirements.txt`, `py train_model.py`, and `py -m streamlit run app.py` without activating the environment.

## Enable GenAI (optional)
1. Visit https://aistudio.google.com/ and check current API/free-tier availability.
2. Rename `.env.example` to `.env`.
3. Add your key after `GEMINI_API_KEY=`.
4. Restart Streamlit. Keep the key private; never upload `.env` to GitHub.
Without a key, classification still works and a built-in explanation is used. Free quotas and model availability can change.

## Dataset
`data/spam.csv` contains a small illustrative set so the project can run immediately. It is only for demonstrating the workflow, not for making claims about real-world accuracy. For stronger results, replace it with a larger legally usable labelled dataset containing columns `text` and `label`. Labels may be `spam` and `ham`. Then rerun `py train_model.py`.

## Architecture
Email input -> TF-IDF -> Naive Bayes -> Spam/Not Spam prediction -> optional Gemini explanation -> Streamlit output.

## Viva notes
- TF-IDF converts text into numeric features based on word importance.
- Naive Bayes is a probabilistic classifier based on Bayes' theorem.
- GenAI creates a human-readable explanation; it does not replace the classifier.
- Streamlit builds the web UI.
- Metrics printed by the training script include precision, recall and F1-score.

## Limitations
The included dataset is small and synthetic/illustrative; model predictions may be wrong. Naive Bayes confidence is not necessarily calibrated. A Not Spam result does not guarantee that an email is safe. The GenAI explanation can also be inaccurate and does not independently verify links. Do not paste confidential emails into third-party APIs. This is an academic prototype, not a production security gateway.
