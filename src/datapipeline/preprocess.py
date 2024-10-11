import pandas as pd
import json
from tqdm import tqdm

# load from local
file_path = "dataset/top.jsonl"

data = []
with open(file_path, "r") as f:
    for line in f:
        data.append(json.loads(line))

df = []
for item in tqdm(data):
    df.append(
        {"question": f"{item['title']} {item['selftext']}", "answer": item["body"]}
    )
df = pd.DataFrame(df)

train_df = df.sample(frac=0.8, random_state=42)
validation_df = df.drop(train_df.index)

train_path = "dataset/train.jsonl"
validation_path = "dataset/validation.jsonl"

train_df.to_json(train_path, orient="records", lines=True)
validation_df.to_json(validation_path, orient="records", lines=True)
