
from pathlib import Path
from email import policy
from email.parser import BytesParser
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw" / "extracted"
OUTPUT = ROOT / "data" / "spam_assassin.csv"


def extract_text(path):
    try:
        with open(path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        parts = []

        subject = msg.get("subject", "")
        if subject:
            parts.append(f"Subject: {subject}")

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    if part.get_content_disposition() == "attachment":
                        continue
                    content = part.get_content()
                    if isinstance(content, str):
                        parts.append(content)
        else:
            if msg.get_content_type() == "text/plain":
                content = msg.get_content()
                if isinstance(content, str):
                    parts.append(content)

        return "\n".join(parts).strip()
    except Exception:
        return ""


rows = []

for path in RAW_DIR.rglob("*"):
    if not path.is_file():
        continue

    # The archive folder names identify the correct labels.
    folder = path.parent.name.lower()

    if "spam" in folder:
        label = "Spam"
    elif "ham" in folder:
        label = "Not Spam"
    else:
        continue

    text = extract_text(path)

    if len(text) >= 20:
        rows.append({"text": text, "label": label})

df = pd.DataFrame(rows, columns=["text", "label"])
if not df.empty:
    df = df.drop_duplicates(subset=["text", "label"])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False, encoding="utf-8")

print("Dataset conversion finished.")
print("Total emails:", len(df))

if not df.empty:
    print("\nClass distribution:")
    print(df["label"].value_counts().to_string())

print("\nSaved to:", OUTPUT)
