import pandas as pd
import re
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('punkt')

# Load spaCy English model for lemmatization
nlp = spacy.load('en_core_web_sm')

# Set of English stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # 3. Remove special characters and emojis
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # 4. Tokenize
    tokens = word_tokenize(text)
    
    # 5. Remove stopwords
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    
    # 6. Lemmatize tokens
    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]
    
    # Return cleaned text as string
    return " ".join(lemmas)

# Load CSV file
df = pd.read_csv('data/joker_comments.csv')

# Apply cleaning with progress bar
tqdm.pandas()
df['cleaned_comment'] = df['comment'].astype(str).progress_apply(clean_text)

# Save cleaned data
df.to_csv('data/joker_comments_cleaned.csv', index=False)

print(df[['comment', 'cleaned_comment']].head())
