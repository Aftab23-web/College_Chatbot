"""Simple diagnostic to write output to file"""
import sys
from datetime import datetime

log_file = "startup_log.txt"

def log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

log("=" * 50)
log("Starting diagnostic...")

try:
    log("1. Testing Flask...")
    from flask import Flask
    log("   ✓ Flask OK")
except Exception as e:
    log(f"   ✗ Flask error: {e}")
    sys.exit(1)

try:
    log("2. Testing NLTK...")
    import nltk
    log("   ✓ NLTK OK")
except Exception as e:
    log(f"   ✗ NLTK error: {e}")
    sys.exit(1)

try:
    log("3. Testing utils.db_manager...")
    from utils.db_manager import DatabaseManager
    log("   ✓ DatabaseManager import OK")
except Exception as e:
    log(f"   ✗ DatabaseManager error: {e}")
    sys.exit(1)

try:
    log("4. Testing utils.nlp_processor...")
    from utils.nlp_processor import NLPProcessor
    log("   ✓ NLPProcessor import OK")
    
    log("5. Initializing NLPProcessor...")
    nlp = NLPProcessor()
    log("   ✓ NLPProcessor initialized OK")
except Exception as e:
    log(f"   ✗ NLPProcessor error: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

try:
    log("6. Loading app.py...")
    import app
    log("   ✓ app.py loaded OK")
except Exception as e:
    log(f"   ✗ app.py error: {e}")
    import traceback
    log(traceback.format_exc())

log("Diagnostic complete!")
log("=" * 50)
