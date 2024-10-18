import json
import os
import pandas as pd
import json
from sklearn.model_selection import train_test_split

# Input and output file paths
jsonl_file = "reddit_500.jsonl"
json_file = "reddit_500.json"

# Read the jsonl file and load it into a list
with open(jsonl_file, "r") as f:
    json_list = [json.loads(line) for line in f]

# Write the list to a json file
with open(json_file, "w") as f:
    json.dump(json_list, f, indent=4)

print(f"Converted {jsonl_file} to {json_file}")

# Read the json file and load it into a list
with open(json_file, "r") as f:
    json_list = json.load(f)

# Write the list to a text file
with open("reddit_500.txt", "w") as f:
    for item in json_list:
        f.write(json.dumps(item) + "\n")

print(f"Converted {json_file} to reddit_500.txt")

# Define constants for local use
INPUT_FILE = "reddit_500.txt"  # Set your input file here
OUTPUT_FOLDER = "data"  # Define your output folder

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def prepare():
    print("prepare()")

    # Process the single input file
    output_file = INPUT_FILE
    print("Processing file:", output_file)

    # Read the contents of the input file
    with open(output_file, "r") as read_file:
        text_response = read_file.read()

    # Clean up the text, removing unnecessary parts
    text_response = text_response.replace("```json", "").replace("```", "")

    # Parse the JSON content from the text
    try:
        json_responses = json.loads(text_response)
        output_pairs = json_responses
    except Exception as e:
        print(f"Error processing the file {output_file}: {e}")
        return

    # Convert to DataFrame and process
    output_pairs_df = pd.DataFrame(output_pairs)
    output_pairs_df.drop_duplicates(subset=["question"], inplace=True)
    output_pairs_df = output_pairs_df.dropna()
    print("Shape:", output_pairs_df.shape)
    print(output_pairs_df.head())

    # Save the dataset as CSV
    filename = os.path.join(OUTPUT_FOLDER, "instruct-dataset.csv")
    output_pairs_df.to_csv(filename, index=False)

    # Build the 'text' column for training
    output_pairs_df["text"] = (
        "human: "
        + output_pairs_df["question"]
        + "\n"
        + "bot: "
        + output_pairs_df["answer"]
    )

    # Prepare the JSONL content
    output_pairs_df["contents"] = output_pairs_df.apply(
        lambda row: [
            {"role": "user", "parts": [{"text": row["question"]}]},
            {"role": "model", "parts": [{"text": row["answer"]}]},
        ],
        axis=1,
    )

    # Split into train and test sets
    df_train, df_test = train_test_split(
        output_pairs_df, test_size=0.1, random_state=42
    )
    df_train[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "train.csv"), index=False)
    df_test[["text"]].to_csv(os.path.join(OUTPUT_FOLDER, "test.csv"), index=False)

    # Limit the test set to 256 samples
    df_test = df_test[:256]

    # Save as JSONL format
    with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
        json_file.write(df_train[["contents"]].to_json(orient="records", lines=True))
    with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
        json_file.write(df_test[["contents"]].to_json(orient="records", lines=True))


if __name__ == "__main__":
    prepare()
