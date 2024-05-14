from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import pandas as pd

import torch
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader, Dataset
import numpy as np

# Load the dataset
df = pd.read_csv('data/train/aws_output_labels.csv')

# Tokenization
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
tokenized_data = tokenizer(df['text'].tolist(), padding=True, truncation=True, max_length=128, return_tensors="pt")

# Split data
train_texts, val_texts, train_labels, val_labels = train_test_split(df['text'], df['label'], test_size=0.1)

# Create datasets
class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_encodings = tokenizer(train_texts.tolist(), truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts.tolist(), truncation=True, padding=True, max_length=128)
train_dataset = TextDataset(train_encodings, train_labels.tolist())
val_dataset = TextDataset(val_encodings, val_labels.tolist())

# Training setup
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # num_labels should match the number of distinct labels

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Start training
trainer.train()

model_path = r"models/Models/turmerik_ml_model"
tokenizer_path = r"models/Tokenizer/turmerik_ml_tokenizer"

# Save the model
model.save_pretrained(model_path)

# Save the tokenizer associated with the model
tokenizer.save_pretrained(tokenizer_path)
