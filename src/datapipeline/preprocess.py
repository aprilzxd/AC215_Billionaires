import json
import os
import pandas as pd
import json
from sklearn.model_selection import train_test_split

# Convert the jsonl file to json
ftype = "train"  # or "test"
jsonl_file = f"dataset/{ftype}.jsonl"
json_file = f"dataset/{ftype}.json"

with open(jsonl_file, "r") as f:
    json_list = [json.loads(line) for line in f]

with open(json_file, "w") as f:
    json.dump(json_list, f, indent=4)

print(f"Converted {jsonl_file} to {json_file}")

# Preprocess the dataset
OUTPUT_FOLDER = "dataset"

with open(json_file, "r") as f:
    output_pairs = json.load(f)
output_pairs_df = pd.DataFrame(output_pairs)
output_pairs_df.drop_duplicates(subset=["question"], inplace=True)
output_pairs_df = output_pairs_df.dropna()
print("Shape:", output_pairs_df.shape)
print(output_pairs_df.head())

filename = os.path.join(OUTPUT_FOLDER, "instruct-dataset.csv")
output_pairs_df.to_csv(filename, index=False)

output_pairs_df["text"] = (
    "human: "
    + output_pairs_df["question"]
    + "\n"
    + "bot: "
    + output_pairs_df["answer"]
)

output_pairs_df["contents"] = output_pairs_df.apply(
    lambda row: [
        {"role": "user", "parts": [{"text": row["question"]}]},
        {"role": "model", "parts": [{"text": row["answer"]}]},
    ],
    axis=1,
)

df_train, df_test = train_test_split(
    output_pairs_df, test_size=0.1, random_state=42
)
df_train[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "train.csv"), index=False)
df_test[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "test.csv"), index=False)

df_test = df_test[:256]

with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
    json_file.write(df_train[["contents"]].to_json(orient="records", lines=True))
with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
    json_file.write(df_test[["contents"]].to_json(orient="records", lines=True))
