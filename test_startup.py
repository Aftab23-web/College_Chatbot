"""Test script to diagnose startup issues"""
import sys
print("Step 1: Python OK")

try:
    from flask import Flask
    print("Step 2: Flask OK")
except Exception as e:
    print(f"Flask error: {e}")
    sys.exit(1)

try:
    import nltk
    print("Step 3: NLTK OK")
except Exception as e:
    print(f"NLTK error: {e}")
    sys.exit(1)

try:
    from utils.nlp_processor import NLPProcessor
    print("Step 4: NLPProcessor import OK")
    nlp = NLPProcessor()
    print("Step 5: NLPProcessor initialized OK")
except Exception as e:
    print(f"NLPProcessor error: {e}")
    sys.exit(1)

try:
    from utils.db_manager import DatabaseManager
    print("Step 6: DatabaseManager import OK")
    db = DatabaseManager()
    print("Step 7: DatabaseManager initialized OK")
except Exception as e:
    print(f"DatabaseManager error: {e}")
    sys.exit(1)

print("\n✓ All imports successful!")
print("Now testing app.py...")

try:
    import app
    print("✓ app.py loaded successfully!")
except Exception as e:
    print(f"✗ app.py error: {e}")
    import traceback
    traceback.print_exc()
