"""Test app startup step by step"""
import sys

print("1. Testing Flask import...")
from flask import Flask
print("   ✓ Flask OK")

print("2. Testing utils imports...")
sys.path.insert(0, '.')
from utils.nlp_processor import NLPProcessor
print("   ✓ NLPProcessor OK")

from utils.db_manager import DatabaseManager
print("   ✓ DatabaseManager OK")

print("3. Testing NLPProcessor initialization...")
nlp = NLPProcessor()
print("   ✓ NLPProcessor initialized")

print("4. Testing DatabaseManager initialization...")
db = DatabaseManager()
print("   ✓ DatabaseManager initialized")

print("\n✓ All components loaded successfully!")
print("Now testing app import...")

import app
print("✓ App imported successfully!")
