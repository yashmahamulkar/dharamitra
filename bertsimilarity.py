import torch
from transformers import AutoTokenizer, AutoModel

# Load the pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Define your input phrases
phrase1 = "Himalaya Purifying Neem Face Wash, 400 Ml"
phrase2 = "Neem Face Wash"

# Tokenize the input phrases and obtain BERT embeddings
tokens1 = tokenizer(phrase1, return_tensors="pt", padding=True, truncation=True)
tokens2 = tokenizer(phrase2, return_tensors="pt", padding=True, truncation=True)

# Obtain BERT embeddings for each phrase
with torch.no_grad():
    output1 = model(**tokens1)
    output2 = model(**tokens2)

# Extract the embeddings for the [CLS] token (used for sentence-level representations)
embedding1 = output1.last_hidden_state[:, 0, :]
embedding2 = output2.last_hidden_state[:, 0, :]

# Compute cosine similarity between the embeddings
cosine_similarity = torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=1)

# Print the cosine similarity score
print("Cosine Similarity:", cosine_similarity.item())



