# This folder contains temporary files that are not tracked by git.

- api_keys.json: Contains the API keys for the LLM provider.
- last_index.txt: Contains the last index of the emails that were processed.
- glove.6B.100d.txt: Contains the GloVe model.

1. Please get the API keys for the LLM provider and put it in the api_keys.json file in the following format:
- Groq: https://console.groq.com/keys

  ```
  {
    "groq_api_key": "<your_groq_api_key#1>","<your_groq_api_key#2>",...
  }
  ```
  These will be cycled through when making LLM calls to avoid rate limiting and to ensure availability of the LLM when populating the `llm_prediction.csv` file.

2. `last_index.txt` is used to keep track of the last index of the emails that were predicted by the LLM. This is used to resume the prediction from the last processed email and thus makes the `llm_prediction.csv` file population function idempotent. This file is updated by the `llm_predictor.ipynb` script and should not be modified manually.

3. Please download the `glove.6B.100d.txt` file from [here](https://nlp.stanford.edu/projects/glove/) and put it in the `tmp` folder.