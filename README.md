# AC215 - Milestone2 - Billionaire Secretary

**Team Members:** Huandong Chang, Mingyuan Ma, Lance Lu, April Zhang

**Group Name:** Billionaires

**Project:** In this project, we aim to develop a platform that automatically connects to a financial database, scrapes data from various online sources, provides analytical and visualization tools, and allows for natural language querying through a chatbot interface. This project aims to reduce the rigidity and repetition in traditional data analysis workflows by providing a more dynamic and automated approach to financial data processing and visualization.

## Milestone2
In this milestone, we implement the components for data management and versioning, model finetuning, and agents.

### Data
Our data is [reddit_finance_43_250k](https://huggingface.co/datasets/winddude/reddit_finance_43_250k), a collection of 250k post/comment pairs from 43 financial, investing and crypto subreddits. Post must have all been text, with a length of 250 chars, and a positive score. Each subreddit is narrowed down to the 70th qunatile before being mergered with their top 3 comments and than the other subs. Further score based methods are used to select the top 250k post/comment pairs. We stored this 680MB dataset in a private Google Cloud Bucket.

### Containers
Our Dockerfiles all follow the standard convention. Run the containers for each component with `sh docker-shell.sh`. For the gemini-finertuner container, Windows users may need to run `bash docker-shell.sh` instead.

### Data Pipeline
Under **`src/datapipeline`:**
1. **`download.py`:** downloads the Reddit data from huggingface as a JSONL file.
2. **`creator.py`:** processes the downloaded data, splits it into train and test sets, and for now takes only the first 500 rows of the data.
3. **`preprocess.py`:** processes the data into the format needed for finetuning.
4. **`upload.py`:** uploads the final data into a Google Cloud Bucket.
5. **`dataloader.py`:** downloads the existing data in the Google Cloud Bucket. Change the `ftype` and `source_blob_name` variables to specify the data to download (length of data, train/test data).

### Front end
Run `pipenv run streamlit run finance_assistant.py --server.address 0.0.0.0` to start the front end, which will be running [here](http://localhost:8501).