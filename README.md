[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
![Platform](https://img.shields.io/badge/Platform-Linux%2C%20Windows%2C%20macOS-blue)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
<a href="https://groq.com" target="_blank" rel="noopener noreferrer">
  <img
    src="https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg"
    alt="Powered by Groq for fast inference."
    width="100" 
  />
</a>
</div>
<br><br>


# The Professional Filter: Machine Learning Approach to Work Email Detection

## Group 6
### Team Members

1. **_Akshay Ashutosh Dongare_**  
__Affiliation__: North Carolina State University, Raleigh, North Carolina, USA  
__Unity ID__: adongar  
__Student ID__: 200600980  
__Emails__: [akshayd02@gmail.com](mailto:akshayd02@gmail.com), [adongar@ncsu.edu](mailto:adongar@ncsu.edu)  


3. **_Ayush Bakul Gala_**  
__Affiliation__: North Carolina State University, Raleigh, North Carolina, USA  
__Unity ID__: agala2  
__Student ID__: 200598694  
__Email__: [agala2@ncsu.edu](mailto:agala2@ncsu.edu)  


1. **_Vidhisha Kamat_**  
__Affiliation__: North Carolina State University, Raleigh, North Carolina, USA  
__Unity ID__: vskamat  
__Student ID__: 200614269  
__Email__: [vskamat@ncsu.edu](mailto:vskamat@ncsu.edu)  

### Final Project Report
Final Project Report is located at `./P6_emailClassification_dataAnalysis.pdf`

## Table of Contents
- [The Proffessional Filter: Machine Learning Approach to Work Email Detection](#the-proffessional-filter-machine-learning-approach-to-work-email-detection)
  - [Group 6](#group-6)
    - [Team Members](#team-members)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Environment Setup](#environment-setup)
    - [Dataset Download](#dataset-download)
    - [Data Processing](#data-processing)
      - [Crawler Script](#crawler-script)
      - [Manually Labelled Subset](#manually-labelled-subset)
      - [Parsing Script](#parsing-script)
    - [tmp Folder](#tmp-folder)
    - [LLM Prediction](#llm-prediction)
    - [Main Script](#main-script)
  - [Project Milestones](#project-milestones)

## Setup

### Environment Setup
- Create a new virtual environment with conda:
  ```bash
  conda create -n g6_alda python=3.12.4
  conda activate g6_alda
  ```
- Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Dataset Download
- Download the Enron email dataset (May 7, 2015 Version) from:
  https://www.cs.cmu.edu/~enron/
- Place the extracted `maildir` folder in `data/raw/`

### Data Processing
- Generate the initial dataset by crawling the raw Enron email dataset:
  ```bash
  python enron_crawler.py
  ```
#### Crawler Script
The crawler script (`enron_crawler.py`) performs the following tasks:
- Recursively traverses through the Enron email dataset directory structure
- Extracts emails from each employee's folders
- For each email:
  - Reads the raw email content
  - Records the employee name (folder owner)
  - Stores the email content
- Outputs a CSV file (`data/crawled/emails.csv`) containing:
  - Employee name
  - Full email message content
- Handles encoding issues and errors gracefully
- Provides progress updates during crawling
- Reports total number of emails processed

#### Manually Labelled Subset
The first 5028 emails from the Enron dataset were manually annotated and stored in `data/annotated/`. Each email was labelled as either:
- 1: Work-related email
- 0: Personal/non-work email

#### Parsing Script
The parsing script (`enron_parser.ipynb`) performs the following tasks:
- Loads the manually labelled email dataset
- Cleans and preprocesses the email data:
  - Removes null values and empty rows
  - Extracts sender email addresses and subjects
  - Calculates email length and number of recipients
  - Extracts email domains and sent timestamps
  - Identifies forwarded emails
- Converts data types appropriately
- Outputs a cleaned DataFrame with features like:
  - Sender email
  - Subject
  - Number of recipients
  - Email length
  - Email domain
  - Sent timestamp
  - Forward status
  - Work/personal label
- Outputs a CSV file (`data/parsed/parsed_emails.csv`) containing the cleaned data

### tmp Folder
- Contains the GloVe model, last index file and the API keys for the LLM provider
- Please refer to the [tmp/README.md](tmp/README.md) for more details.
- Follow the instructions and set it up properly before running the `llm_predictor.ipynb` and `main.ipynb` scripts.

### LLM Prediction
The LLM prediction script (`llm_predictor.ipynb`) performs the following operations:
- Retrieves the preprocessed email dataset from `data/parsed/parsed_emails.csv`, ensuring idempotence through the use of a `last_index.txt` file which records the last processed email to prevent reprocessing.
- Initializes the Groq LLM classifier with:
  - The dataset path.
  - API key configurations from `./tmp/api_keys.json`, implementing API key cycling to manage usage limits and ensure continuous operation.
- Processes each email by:
  - Extracting key features such as subject, content, and metadata.
  - Crafting a system prompt based on research guidelines to accurately determine the nature of the email (work-related or personal).
  - Sending this prompt to the Groq LLM API for classification.
  - Receiving a binary classification indicating the nature of the email.
  - Employing guardrails from `llm_predictor_module.py` to validate the API response, ensuring the output is either '1' (work-related) or '0' (personal), and reasking as necessary.
- Compiles and records predictions for each email, categorizing them as:
  - 1: Work-related email.
  - 0: Personal/non-work email.
- Outputs the results to `data/llm/llm_prediction.csv`.
- Provides detailed validation outcomes for each prediction to ensure traceability and compliance with expected formats.
- Ensures atomicity in operations to maintain data integrity throughout the prediction process.
- Manages API rate limits and handles any errors robustly, ensuring smooth operation under varying network conditions and API response scenarios.

### Main Script
- The main script (`main.ipynb`) conducts a comprehensive analysis and modeling process on the preprocessed email dataset.
- Implements various machine learning models:
  - Support Vector Machines (SVM)
  - Random Forests
  - AdaBoost
  - Deep Neural Network (DNN)
- Evaluates the performance of the above models.
- Includes the evaluation of the LLM-based classifier for comparison.
- Utilizes Grid Search to optimize model parameters.
- Contains data visualization and analysis code.

## Project Milestones

- [x] **Environment Setup**
- [x] **Dataset Acquisition and Preparation**
- [x] **Manual Labelling**
- [x] **Data Processing**
- [x] **Machine Learning Model Development**
- [x] **Model Training and Evaluation**
- [x] **LLM Prediction Implementation**
- [x] **Project Documentation and Reporting**
