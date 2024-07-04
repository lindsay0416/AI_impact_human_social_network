# Clustering: https://scikit-learn.org/stable/modules/clustering.html#clustering
# Use LLM to extract the aspect and opinion.
# Use prompt engineering to improve the accuracy of LLM's output.

# Aspects: Extract from the original topcis.
# Opinion: Extract from the original comments and simulation results
# Cluster the opinion in the original comments and simulation results
# Profile analysis: 
# 1. Profiles of positive opinion for each topic, 
# 2. Profiles of negative opinion for each topicn, 
# 3. profile each cluster

# https://huggingface.co/siebert/sentiment-roberta-large-english

# Import required packages
import os
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

# Enforce using CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Create class for data preparation
class SimpleDataset:
    def __init__(self, tokenized_texts):
        self.tokenized_texts = tokenized_texts
    
    def __len__(self):
        return len(self.tokenized_texts["input_ids"])
    
    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.tokenized_texts.items()}
    
def main():
    # Load tokenizer and model, create trainer
    model_name = "siebert/sentiment-roberta-large-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    trainer = Trainer(model=model)

    # Create list of texts (can be imported from .csv, .xls etc.)
    pred_texts = ['I like that', 'That is annoying', 'This is great!', 'Wouldn´t recommend it.']

    # Tokenize texts and create prediction data set
    tokenized_texts = tokenizer(pred_texts, truncation=True, padding=True)
    pred_dataset = SimpleDataset(tokenized_texts)

    # Run predictions
    predictions = trainer.predict(pred_dataset)

    # Transform predictions to labels
    preds = predictions.predictions.argmax(-1)
    labels = pd.Series(preds).map(model.config.id2label)
    scores = (np.exp(predictions[0]) / np.exp(predictions[0]).sum(-1, keepdims=True)).max(1)

    # Create DataFrame with texts, predictions, labels, and scores
    df = pd.DataFrame(list(zip(pred_texts, preds, labels, scores)), columns=['text', 'pred', 'label', 'score'])
    print(df.head())

if __name__ == '__main__':
    main()
