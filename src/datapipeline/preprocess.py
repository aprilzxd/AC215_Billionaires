import pandas as pd
import json
import unidecode
import argparse
import sys
import os
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def contains_link_or_emoji(text):
    # Check for URLs using regex
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Check for emojis
    emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F900-\U0001F9FF\U0001FA00-\U0001FAFF\U00002700-\U000027BF]'
    return text.str.contains(url_pattern, regex=True) | text.str.contains(emoji_pattern, regex=True)

def clean_special_signs(text):
    # Define replacements for HTML entities and special characters
    replacements = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'",
        '&nbsp;': ' ',
        '\xa0': ' ',
        '\u200B': '',
        '©': 'copyright',
        '®': 'registered',
        '™': 'trademark',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Convert non-ASCII characters to their closest ASCII representation
    text = unidecode.unidecode(text)
    
    return text

def preprocess(sample_size):
    # Load from local
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
    
    df = pd.DataFrame(df).drop_duplicates().dropna()
    df = df[~contains_link_or_emoji(df['question']) & ~contains_link_or_emoji(df['answer'])]
    df = df.sample(n=sample_size, random_state=42)
    df['question'] = df['question'].apply(clean_special_signs)
    df['answer'] = df['answer'].apply(clean_special_signs)
    df = df.reset_index(drop=True)

    df["text"] = (
        "human: "
        + df["question"]
        + "\n"
        + "bot: "
        + df["answer"]
    )

    df["contents"] = df.apply(
        lambda row: [
            {"role": "user", "parts": [{"text": row["question"]}]},
            {"role": "model", "parts": [{"text": row["answer"]}]},
        ],
        axis=1,
    )

    df_train, df_test = train_test_split(
        df, test_size=0.2, random_state=42
    )

    with open(os.path.join(OUTPUT_FOLDER, "train.jsonl"), "w") as json_file:
        json_file.write(df_train[["contents"]].to_json(orient="records", lines=True))
    with open(os.path.join(OUTPUT_FOLDER, "test.jsonl"), "w") as json_file:
        json_file.write(df_test[["contents"]].to_json(orient="records", lines=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Specify the sample size (500, 1000, etc.).")
    parser.add_argument("sample_size", help="Specify the sample size: 500, 1000, etc.")
    args = parser.parse_args()

    try:
        sample_size = int(args.sample_size)
    except ValueError:
        print("Error: Please enter a valid integer for the sample size.")
        sys.exit(1)

    OUTPUT_FOLDER = "dataset"
    preprocess(sample_size)
