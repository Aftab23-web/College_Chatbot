"""
NLP Processor Module
Handles text preprocessing for the chatbot using NLTK
"""

import re
import string

# Import only specific NLTK modules to avoid compatibility issues
try:
    import nltk.data
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    nltk_available = True
except ImportError:
    nltk_available = False
    print("⚠ NLTK not fully available")

class NLPProcessor:
    """
    NLP preprocessing class for text cleaning and normalization
    """
    
    def __init__(self):
        """Initialize NLTK components"""
        if not nltk_available:
            print("⚠ NLP features limited - NLTK not available")
            self.lemmatizer = None
            self.stop_words = set()
            return
            
        self.lemmatizer = WordNetLemmatizer()
        
        # Download required NLTK data (run once)
        # Handle punkt for tokenization
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            import nltk as nltk_download
            nltk_download.download('punkt', quiet=True)
        
        # Handle punkt_tab for newer NLTK versions
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except (LookupError, OSError):
            try:
                import nltk as nltk_download
                nltk_download.download('punkt_tab', quiet=True)
            except:
                pass
        
        # Handle stopwords
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            import nltk as nltk_download
            nltk_download.download('stopwords', quiet=True)
        
        # Handle wordnet
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            import nltk as nltk_download
            nltk_download.download('wordnet', quiet=True)
        
        # Handle omw-1.4 (Open Multilingual Wordnet)
        try:
            nltk.data.find('corpora/omw-1.4')
        except LookupError:
            try:
                import nltk as nltk_download
                nltk_download.download('omw-1.4', quiet=True)
            except:
                pass
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            # Fallback if stopwords fail
            self.stop_words = set()
    
    def clean_text(self, text):
        """
        Clean and normalize text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits (keep only letters and spaces)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text):
        """
        Tokenize text into words
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of tokens
        """
        if not nltk_available:
            # Fallback to simple split if NLTK not available
            return text.split()
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """
        Remove stop words from tokens
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Filtered tokens
        """
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Lemmatize tokens to their root form
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Lemmatized tokens
        """
        if not nltk_available or self.lemmatizer is None:
            # Return tokens as-is if lemmatizer not available
            return tokens
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        # Clean text
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stop words
        tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        tokens = self.lemmatize(tokens)
        
        # Join back to string
        return ' '.join(tokens)
    
    def preprocess_batch(self, texts):
        """
        Preprocess multiple texts
        
        Args:
            texts (list): List of text strings
            
        Returns:
            list: List of preprocessed texts
        """
        return [self.preprocess(text) for text in texts]


# Example usage
if __name__ == "__main__":
    processor = NLPProcessor()
    
    sample_text = "Hello! How can I apply for the admission process in 2024?"
    processed = processor.preprocess(sample_text)
    
    print("Original:", sample_text)
    print("Processed:", processed)
    
    # Test batch processing
    texts = [
        "What is the fee structure?",
        "Tell me about placement opportunities",
        "How do I contact the admission office?"
    ]
    
    processed_batch = processor.preprocess_batch(texts)
    print("\nBatch Processing:")
    for original, processed in zip(texts, processed_batch):
        print(f"  {original} -> {processed}")
