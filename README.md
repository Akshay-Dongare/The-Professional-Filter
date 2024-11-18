# G6_ALDA_Project

## Team Members
- Akshay Ashutosh Dongare 
- Ayush Bakul Gala
- Vidhisha Kamat

## Setup
- Install Python 3.10 or above
- Make a new virual environment with conda
  - `conda create -n g6_alda python=3.12.4`
  - `conda activate g6_alda`
- Install all the libraries from the requirements.txt file
  - `pip install -r requirements.txt`
- Download the dataset from the link given below and put it (maildir folder) in the `data/raw` folder
  - https://www.cs.cmu.edu/~enron/ (May 7, 2015 Version)
- Create an `emails.csv` file in a `data/crawled` folder
- Next, execute the  `enron_crawler.py` script to generate the crawled dataset
- Then run the `enron_parser.py` to extract features

## Project Plan
- [x] Dataset Crawler
- [x] Dataset Parsing
- [ ] Dataset Labelling
- [ ] Data Cleaning
- [ ] Data Analysis
- [ ] Data Visualization
- [ ] Model Training
- [ ] Model Evaluation
- [ ] Model Testing
