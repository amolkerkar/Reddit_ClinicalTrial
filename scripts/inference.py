import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Surety threshold for potential candidates ajust as per ur need
surety_threshold = 0.65

#Loading the model and tokenizer
model_path = r"models/Models/turmerik_ml_model"
tokenizer_path = r"models/Tokenizer/turmerik_ml_tokenizer"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
model.eval()

#GPU/CPU
if torch.cuda.is_available():
    model.to("cuda")

df = pd.read_csv('data/test/test_data_cleaned.csv')

# Prediction
def predict(text):
    
    inputs = tokenizer(text, return_tensors="pt", max_length=128, truncation=True, padding='max_length', add_special_tokens=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    # Eval
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return probs

# potential candidates storage
candidates = []

#Inference
for index, row in df.iterrows():
    probs = predict(row['comment'])
    if probs[0, 1] > surety_threshold:
        candidates.append({
            "author_id": row['author_id'],
            "comment": row['comment']
        })

candidates_df = pd.DataFrame(candidates)

candidates_df.to_csv('output/final_potential_candidates.csv', index=False)
print("Potential candidates saved to 'output/final_potential_candidates.csv'.")
