# Clustering: https://scikit-learn.org/stable/modules/clustering.html#clustering

import spacy
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return tokens

def extract_aspects(text):
    doc = nlp(text)
    aspects = []
    for token in doc:
        if token.dep_ == 'amod':  # Adjective modifier
            aspects.append((token.head.text, token.text))
        elif token.dep_ == 'nsubj' and token.head.pos_ == 'VERB':  # Subject noun
            aspects.append(token.text)
    return aspects

def get_bert_embedding(aspect):
    # Tokenize and encode the aspect
    inputs = tokenizer(aspect, return_tensors='pt')
    # Get the hidden states from BERT
    with torch.no_grad():
        outputs = model(**inputs)
    # Get the embeddings of the [CLS] token
    cls_embedding = outputs.last_hidden_state[0, 0, :].numpy()
    return cls_embedding

def cluster_aspects(embeddings, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(embeddings)
    return kmeans.labels_

   

if __name__ == '__main__':
     # Example usage
    comments = [
        "The new policy is beneficial",
        "The government decision is controversial",
        # Add more comments here...
    ]

    preprocessed_comments = [preprocess(comment) for comment in comments]
    all_aspects = [extract_aspects(comment) for comment in preprocessed_comments]
    flat_aspects = [aspect for sublist in all_aspects for aspect in sublist]

    # Get BERT embeddings for all aspects
    aspect_texts = [' '.join(aspect) if isinstance(aspect, tuple) else aspect for aspect in flat_aspects]
    embeddings = np.array([get_bert_embedding(aspect) for aspect in aspect_texts])

    # Perform PCA to reduce dimensionality (optional but recommended for clustering)
    pca = PCA(n_components=50)
    reduced_embeddings = pca.fit_transform(embeddings)

    # Cluster the aspects
    num_clusters = 5
    labels = cluster_aspects(reduced_embeddings, num_clusters)

    # Print clustering results
    for aspect, label in zip(flat_aspects, labels):
        print(f"Aspect: {aspect} - Cluster: {label}")