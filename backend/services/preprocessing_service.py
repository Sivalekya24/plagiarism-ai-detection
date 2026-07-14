import re
import unicodedata
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize


# Download resources only if they are missing
resources = {
    "tokenizers/punkt": "punkt",
    "tokenizers/punkt_tab": "punkt_tab",
    "corpora/stopwords": "stopwords",
    "corpora/wordnet": "wordnet",
    "corpora/omw-1.4": "omw-1.4"
}

for resource_path, resource_name in resources.items():
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name)


class PreprocessingService:

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text: str):

        # Normalize unicode characters
        text = unicodedata.normalize("NFKC", text)

        # Convert to lowercase
        text = text.lower()

        # Save original text for sentence matching
        original_text = text

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Remove punctuation
        text = re.sub(r"[^\w\s]", " ", text)

        # Tokenize words
        words = word_tokenize(text)

        # Remove stopwords and lemmatize
        processed_words = []

        for word in words:

            if word not in self.stop_words:

                processed_words.append(
                    self.lemmatizer.lemmatize(word)
                )

        cleaned_text = " ".join(processed_words)

        # Sentence tokenization (before punctuation removal)
        sentences = sent_tokenize(original_text)

        return {
            "cleaned_text": cleaned_text,
            "sentences": sentences
        }