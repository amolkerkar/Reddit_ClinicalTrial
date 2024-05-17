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
## How I trained my model
- `train_data_extractor.py` with desired comment limit
- `train_data_cleaning.py`
-  Uploaded the output csv file to AWS S3 and labelled using AWS SageMaker and exported as .manifest file
-  Ran the script manifest_to_csv.py to get the labelled csv which was feed to the BERT model for finetuning in model_trainer.py

## How to Use

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
2. Update the OpenAI API key in
- `scripts/keyfile.py`

3. Download the model file, unzip and put it in the models folder:
   https://drive.google.com/file/d/1ERBW_ayibTyQkU4OGwMAU5acH7EhJDGR/view?usp=drive_link
   
5. Update the Praw client ID and secret ID in files:
- `test_data_extractor.py`
- `train_data_extractor.py`
5. Run this file to get the updated test data, make sure to edit the number of posts and comments desired in the script
- `test_data_extractor.py` followed by
- `test_data_cleaning.py`
6. Run this file to get the final_potential_candidates.csv
- `inference.py`
7. Run this script to get the messages generated in recruitment_messages.csv
- `message_generator.py`

## Example of messages genrated:
### *Data flow in the file is as follows : author_id,comment,sentiment_polarity,sentiment_subjectivity,personalized_message*
 Usernamehidden
- "i can’t answer any specifics because it’s been so long but i love giving my  cents, because i was engaged in the low carb universe back in the day  low carb diets can ramp up your cortisol and make you feel like you have more energy and even some euphoria, but from what i can tell, it’s rarely sustainable.  i rode that high for a couple of months  years ago. it was a wired, anxiety ridden energy. almost what i’d imagine an extremely small dose of meth might feel like. i don’t think i was drinking any coffee at the time. i was at college and rarely had to get up early so there was no need"
- 0.14181818181818182,
- 0.46727272727272723,
- "Hello,Thank you for sharing your experience with low carb diets and its effects on energy levels and anxiety. Your insight is valuable in understanding the impact of different dietary approaches on our well-being.I wanted to reach out to you about a clinical trial related to caffeine intake and anxiety. Your perspective on how certain dietary choices can influence energy levels and mood could be incredibly beneficial in our research. Would you be open to participating in our study and sharing your thoughts on this topic?

*Usernamehidden*,
- "i've been primal/paleo diet (high fat, moderate protein, low carb) for  weeks now and decaf for / weeks. i wouldn't correlate any together. i feel amazing since changing to this diet/lifestyle and i've lost over a stone in weight (i had already started losing weight after stopping caffeine. i was -kg kilos when stopping caffeine  weeks ago, -kg when starting the primal diet  weeks ago and now i'm around -kg. i’m rapidly losing fat whilst retaining muscle. my energy and satiety levels are amazing!  i stopped caffeine because of panic attacks/anxiety. i wrote a post about it. caffeine definitely caused/contributed to me having anxiety. my anxiety has completely disappeared now ☺️",
- 0.20125000000000004,
- 0.5425,
- "Hello, I hope this message finds you well. I couldn't help but notice your incredible journey towards better health and wellbeing through your primal/paleo diet and giving up caffeine. It's truly inspiring to hear how positively these changes have impacted your life, especially in regards to managing your anxiety. I wanted to reach out to you about a clinical trial related to caffeine intake and anxiety. Your unique experience and insights could provide valuable contributions to our understanding of this topic. Your participation could"

## Ethical considererations:
- Reddit usernames were hidden when dispalying the results anywhere on the internet
- Some Subreddits have strict rules of not messaging the users for a research interest, those subreddits were not considered for data extraction
- There was a pause introduced in data extraction algorithm adhering the reddit apis limit of data parsing rules
