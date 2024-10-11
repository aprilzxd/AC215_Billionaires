import pandas as pd

df = pd.read_json("hf://datasets/winddude/reddit_finance_43_250k/top.jsonl", lines=True)
df.to_json("dataset/top.jsonl", orient='records', lines=True)
