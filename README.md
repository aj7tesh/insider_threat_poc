# Insider Threat (POC)
POC implementation for "A Machine Learning Approach to Detect Insider Threats
in Emails Caused by Human Behaviours"

## Prerequisites
- python 3.6 +

Install various python libraries as mentioned in requirements.txt file with upgraded pip

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```
Download stopwords and words from nltk using below commands

```bash
python -m nltk.downloader stopwords
python -m nltk.downloader words
```

## Implementation
Step 1: Data Preparation
This method implements below steps from paper
 -  Implements email normalization steps mentioned in paper
    1. Email -> Email body
    2. Lowercasing
    3. Tokenization
    4. Contraction Removal
    5. Punctuation Removal
    6. Repeated Characters Replacement
    7. Stopwords removal
    8. Stemming 
    9. Spellcheck  
    10. Final csv file with normalized data

## Usage
Run main.py or script.sh to execute step-1 of this POC

```bash
python main.py
sh script.sh 
```