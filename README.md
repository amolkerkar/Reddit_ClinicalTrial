# Sentiment Analysis and Personalized Messaging for Clinical Trial Recruitment

## Project Structure

- `data/`
  - `test/`: Contains test data files.
  - `train/`: Contains training data files.
- `logs/`: Directory for log files.
- `models/`: Directory for model files.
- `output/`: Directory for final output files.
- `results/`: Directory for result files.
- `scripts/`: Directory for all Python scripts.

## Scripts

- `inference.py`: Script for running inference.
- `keyfile.py`: Contains the API key.
- `manifest_to_csv.py`: Converts manifests to CSV.
- `message_generator.py`: Generates personalized messages.
- `model_trainer.py`: Trains the model.
- `test_data_cleaning.py`: Cleans test data.
- `test_data_extractor.py`: Extracts test data.
- `train_data_cleaning.py`: Cleans training data.
- `train_data_extractor.py`: Extracts training data.

## How to Use

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
2. Update the OpenAI API key in
- `scripts/keyfile.py`
4. Update the Praw client ID and secret ID in files:
- `test_data_extractor.py`
- `train_data_extractor.py`
5. Run this file to get the updated test data, make sure to edit the number of posts and comments desired in the script
- `test_data_extractor.py` followed by
- `test_data_cleaning.py`
6. Run this file to get the final_potential_candidates.csv
- `inference.py`
7. Run this script to get the messages generated in recruitment_messages.csv
- `message_generator.py`

