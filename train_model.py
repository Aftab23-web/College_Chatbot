"""
Machine Learning Model Training Script
Trains intent classification model using TF-IDF and Logistic Regression
"""

import sys
import io

# Set UTF-8 encoding for stdout to handle emoji and special characters
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    classification_report,
    confusion_matrix
)
import warnings
warnings.filterwarnings('ignore')

# Import custom NLP processor
from utils.nlp_processor import NLPProcessor

class IntentClassifier:
    """
    Intent Classification Model using TF-IDF + Logistic Regression
    """
    
    def __init__(self):
        """Initialize model components"""
        self.nlp_processor = NLPProcessor()
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 3),  # Unigrams, bigrams, and trigrams
            min_df=1,
            max_df=0.8,
            sublinear_tf=True
        )
        self.classifier = LogisticRegression(
            max_iter=2000,
            random_state=42,
            solver='lbfgs',
            C=10.0,
            class_weight='balanced'
        )
        self.intent_labels = []
    
    def load_data(self, filepath='intents.json'):
        """
        Load training data from JSON file
        
        Args:
            filepath (str): Path to intents.json
            
        Returns:
            tuple: (patterns, labels)
        """
        print(f" Loading training data from {filepath}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        patterns = []
        labels = []
        
        for intent in data['intents']:
            tag = intent['tag']
            for pattern in intent['patterns']:
                patterns.append(pattern)
                labels.append(tag)
        
        print(f"✓ Loaded {len(patterns)} patterns across {len(set(labels))} intents")
        return patterns, labels
    
    def preprocess_data(self, patterns):
        """
        Preprocess text data using NLP processor
        
        Args:
            patterns (list): List of text patterns
            
        Returns:
            list: Preprocessed patterns
        """
        print(" Preprocessing text data...")
        preprocessed = self.nlp_processor.preprocess_batch(patterns)
        print(f"✓ Preprocessed {len(preprocessed)} patterns")
        return preprocessed
    
    def train(self, patterns, labels, test_size=0.15):
        """
        Train the intent classification model
        
        Args:
            patterns (list): Training patterns
            labels (list): Intent labels
            test_size (float): Test set size for evaluation
            
        Returns:
            dict: Training metrics
        """
        print("\nTraining Intent Classification Model...")
        print("=" * 60)
        
        # Preprocess patterns
        preprocessed_patterns = self.preprocess_data(patterns)
        
        # Store unique intent labels
        self.intent_labels = sorted(list(set(labels)))
        print(f" Intent Classes: {len(self.intent_labels)}")
        
        # Check if we have enough data for test split (need at least 2 samples per class for stratified split)
        min_samples_needed = len(self.intent_labels) * 2
        if len(patterns) < min_samples_needed or len(patterns) * test_size < len(self.intent_labels):
            print(f"  Small dataset ({len(patterns)} patterns, {len(self.intent_labels)} classes): Using entire dataset for training and testing")
            X_train = preprocessed_patterns
            y_train = labels
            X_test = preprocessed_patterns
            y_test = labels
        else:
            # Split data for evaluation
            X_train, X_test, y_train, y_test = train_test_split(
                preprocessed_patterns, 
                labels, 
                test_size=test_size, 
                random_state=42,
                stratify=labels
            )
        
        print(f" Training samples: {len(X_train)}")
        print(f" Testing samples: {len(X_test)}")
        
        # TF-IDF Vectorization
        print("\n Creating TF-IDF features...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        print(f"✓ Feature dimensions: {X_train_tfidf.shape[1]}")
        
        # Train classifier
        print("\n Training Logistic Regression classifier...")
        self.classifier.fit(X_train_tfidf, y_train)
        print("✓ Model training completed")
        
        # Predictions
        y_pred = self.classifier.predict(X_test_tfidf)
        
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.classifier, 
            X_train_tfidf, 
            y_train, 
            cv=5, 
            scoring='accuracy'
        )
        metrics['cv_mean'] = cv_scores.mean()
        metrics['cv_std'] = cv_scores.std()
        
        # Print evaluation
        self._print_evaluation(metrics, y_test, y_pred)
        
        return metrics
    
    def _print_evaluation(self, metrics, y_test, y_pred):
        """Print detailed evaluation metrics"""
        print("\n" + "=" * 60)
        print(" MODEL EVALUATION RESULTS")
        print("=" * 60)
        print(f"Accuracy:           {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
        print(f"Precision:          {metrics['precision']:.4f}")
        print(f"Recall:             {metrics['recall']:.4f}")
        print(f"F1-Score:           {metrics['f1_score']:.4f}")
        print(f"Cross-Val Accuracy: {metrics['cv_mean']:.4f} (±{metrics['cv_std']:.4f})")
        print("=" * 60)
        
        # Classification report
        print("\n DETAILED CLASSIFICATION REPORT:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # Confusion matrix
        print("\n CONFUSION MATRIX:")
        cm = confusion_matrix(y_test, y_pred, labels=self.intent_labels)
        print(cm)
    
    def predict(self, text, return_confidence=False):
        """
        Predict intent for input text
        
        Args:
            text (str): Input text
            return_confidence (bool): Return confidence scores
            
        Returns:
            str or tuple: Predicted intent (and confidence if requested)
        """
        # Preprocess
        processed = self.nlp_processor.preprocess(text)
        
        # Vectorize
        text_tfidf = self.vectorizer.transform([processed])
        
        # Predict
        prediction = self.classifier.predict(text_tfidf)[0]
        
        if return_confidence:
            # Get probability scores
            proba = self.classifier.predict_proba(text_tfidf)[0]
            confidence = max(proba)
            return prediction, confidence
        
        return prediction
    
    def save_model(self, model_dir='models'):
        """
        Save trained model and vectorizer
        
        Args:
            model_dir (str): Directory to save models
        """
        os.makedirs(model_dir, exist_ok=True)
        
        classifier_path = os.path.join(model_dir, 'intent_classifier.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        # Save classifier
        with open(classifier_path, 'wb') as f:
            pickle.dump(self.classifier, f)
        print(f"✓ Saved classifier to {classifier_path}")
        
        # Save vectorizer
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"✓ Saved vectorizer to {vectorizer_path}")
        
        # Save intent labels
        labels_path = os.path.join(model_dir, 'intent_labels.pkl')
        with open(labels_path, 'wb') as f:
            pickle.dump(self.intent_labels, f)
        print(f"✓ Saved intent labels to {labels_path}")
    
    def load_model(self, model_dir='models'):
        """
        Load trained model and vectorizer
        
        Args:
            model_dir (str): Directory containing models
        """
        classifier_path = os.path.join(model_dir, 'intent_classifier.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        labels_path = os.path.join(model_dir, 'intent_labels.pkl')
        
        # Load classifier
        with open(classifier_path, 'rb') as f:
            self.classifier = pickle.load(f)
        
        # Load vectorizer
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        # Load intent labels
        with open(labels_path, 'rb') as f:
            self.intent_labels = pickle.load(f)
        
        print(f"✓ Model loaded from {model_dir}")


def main():
    """Main training function"""
    print("\n" + "=" * 60)
    print("AI CHATBOT - INTENT CLASSIFICATION TRAINING")
    print("=" * 60 + "\n")
    
    # Initialize classifier
    classifier = IntentClassifier()
    
    # Load data
    patterns, labels = classifier.load_data('intents.json')
    
    # Train model
    metrics = classifier.train(patterns, labels)
    
    # Save model
    print("\n Saving trained model...")
    classifier.save_model()
    
    print("\n" + "=" * 60)
    print(" TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    # Test predictions
    print("\n Testing Sample Predictions:")
    print("-" * 60)
    
    test_queries = [
        "Hello, how are you?",
        "What is the fee structure?",
        "Tell me about placements",
        "How can I contact you?"
    ]
    
    for query in test_queries:
        intent, confidence = classifier.predict(query, return_confidence=True)
        print(f"Query: '{query}'")
        print(f"  → Intent: {intent} (Confidence: {confidence:.4f})")
        print()
    
    print("=" * 60)
    print(" Model is ready to use!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
