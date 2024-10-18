# AC215 - Milestone2 - Billionaire Secretary

**Team Members**
Huandong Chang, Mingyuan Ma, Lance Lu, April Zhang

**Group Name**
Billionaires

**Project**
In this project, we aim to develop a platform that automatically connects to a financial database, scrapes data from various online sources, provides analytical and visualization tools, and allows for natural language querying through a chatbot interface. This project aims to reduce the rigidity and repetition in traditional data analysis workflows by providing a more dynamic and automated approach to financial data processing and visualization.

## Milestone2
In this milestone, we implement the components for data management and versioning, model finetuning, and agents.

### Data
Our data is [reddit_finance_43_250k](https://huggingface.co/datasets/winddude/reddit_finance_43_250k), a collection of 250k post/comment pairs from 43 financial, investing and crypto subreddits. Post must have all been text, with a length of 250 chars, and a positive score. Each subreddit is narrowed down to the 70th qunatile before being mergered with their top 3 comments and than the other subs. Further score based methods are used to select the top 250k post/comment pairs. We stored this 680MB dataset in a private Google Cloud Bucket.

### Data Pipeline Overview
Under `src/datapipeline`:
1. **`download.py`, `preprocess.py`, and `upload.py`**
   These scripts download the data from huggingface, preprocess them into the format needed for finetuning, and upload them into a  Google Cloud Bucket. We currently reduced the dataset to 500 rows and splitted them into train and test sets.

2. **`dataloader.py`**
   This script downloads the existing data in the Google Cloud Bucket.

3. **`Pipfile`**
   We used the following packages to help with preprocessing:
   - `pandas`
   - `tqdm`
   - `google-cloud-storage`
   - `fsspec`
   - `huggingface_hub`

4. **`Dockerfile`**
   Our Dockerfiles all follow the standard convention. Run the containers with `sh docker-shell.sh`. For the container for gemini-finertuner, Windows users may need to run `bash docker-shell.sh`.
