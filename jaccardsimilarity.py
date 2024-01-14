from nltk.metrics import jaccard_distance

# Function to calculate Jaccard similarity between two strings
def jaccard_similarity(str1, str2):
    # Tokenize the strings into sets of words
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    
    # Calculate Jaccard similarity
    similarity = 1 - jaccard_distance(set1, set2)
    return similarity

# Example usage
phrase1 = "Himalaya Purifying Neem Face Wash, 400 Ml"
phrase2 = " Neem Face Wash, 400 Ml"
similarity = jaccard_similarity(phrase1, phrase2)
print(f"Jaccard Similarity between '{phrase1}' and '{phrase2}': {similarity:.2f}")
