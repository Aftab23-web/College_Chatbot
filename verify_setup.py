"""
System Verification Script
Run this after setup to verify all components are working
"""

import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print("\n Checking Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f" Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f" Python {version.major}.{version.minor} - Need 3.8+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n Checking Dependencies...")
    
    required_packages = [
        'flask',
        'sklearn',
        'nltk',
        'mysql.connector',
        'bcrypt',
        'speech_recognition',
        'pyttsx3',
        'dotenv'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            elif package == 'sklearn':
                __import__('sklearn')
            elif package == 'speech_recognition':
                __import__('speech_recognition')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"   {package}")
        except ImportError:
            print(f"   {package} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_nltk_data():
    """Check if NLTK data is downloaded"""
    print("\n Checking NLTK Data...")
    
    try:
        import nltk
        
        required_data = ['punkt', 'stopwords', 'wordnet']
        all_present = True
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}') if data == 'punkt' else nltk.data.find(f'corpora/{data}')
                print(f"   {data}")
            except LookupError:
                print(f"   {data} - NOT DOWNLOADED")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"   Error: {e}")
        return False

def check_database():
    """Check database connection"""
    print("\n Checking Database Connection...")
    
    try:
        import mysql.connector
        from dotenv import load_dotenv
        
        load_dotenv()
        
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'chatbot_db')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            required_tables = ['intents', 'responses', 'chat_logs', 'admin_users']
            found_tables = [table[0] for table in tables]
            
            print(f"   Connected to database")
            
            for table in required_tables:
                if table in found_tables:
                    print(f"   Table '{table}' exists")
                else:
                    print(f"   Table '{table}' missing")
            
            # Check sample data
            cursor.execute("SELECT COUNT(*) FROM intents")
            intent_count = cursor.fetchone()[0]
            print(f"    Intents in database: {intent_count}")
            
            cursor.execute("SELECT COUNT(*) FROM responses")
            response_count = cursor.fetchone()[0]
            print(f"    Responses in database: {response_count}")
            
            cursor.close()
            connection.close()
            return True
    except Exception as e:
        print(f"   Database Error: {e}")
        print(f"   Tip: Check MySQL is running and credentials in .env file")
        return False

def check_model_files():
    """Check if ML model files exist"""
    print("\n Checking ML Model Files...")
    
    model_dir = 'models'
    required_files = [
        'intent_classifier.pkl',
        'vectorizer.pkl',
        'intent_labels.pkl'
    ]
    
    all_present = True
    
    for file in required_files:
        file_path = os.path.join(model_dir, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   {file} ({size} bytes)")
        else:
            print(f"   {file} - NOT FOUND")
            all_present = False
    
    if not all_present:
        print(f"   Tip: Run 'python train_model.py' to generate model files")
    
    return all_present

def check_intents_file():
    """Check if intents.json exists"""
    print("\n Checking Training Data...")
    
    if os.path.exists('intents.json'):
        try:
            import json
            with open('intents.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                intent_count = len(data.get('intents', []))
                
                total_patterns = 0
                for intent in data.get('intents', []):
                    total_patterns += len(intent.get('patterns', []))
                
                print(f"   intents.json found")
                print(f"    Intents: {intent_count}")
                print(f"    Training patterns: {total_patterns}")
                return True
        except Exception as e:
            print(f"   Error reading intents.json: {e}")
            return False
    else:
        print(f"   intents.json not found")
        return False

def check_env_file():
    """Check if .env file is configured"""
    print("\n Checking Configuration...")
    
    if os.path.exists('.env'):
        print(f"   .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check important variables
        db_password = os.getenv('DB_PASSWORD', '')
        secret_key = os.getenv('SECRET_KEY', '')
        
        if not db_password:
            print(f"    DB_PASSWORD is empty - update in .env file")
        else:
            print(f"   DB_PASSWORD is set")
        
        if 'change' in secret_key.lower() or not secret_key:
            print(f"    SECRET_KEY needs to be changed")
        else:
            print(f"   SECRET_KEY is set")
        
        return True
    else:
        print(f"   .env file not found")
        print(f"   Tip: Copy .env.example to .env and configure")
        return False

def test_nlp_processing():
    """Test NLP preprocessing"""
    print("\n📌 Testing NLP Processing...")
    
    try:
        from utils.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        test_text = "Hello! How can I apply for admission?"
        processed = processor.preprocess(test_text)
        
        print(f"   NLP Processor initialized")
        print(f"   Test input: '{test_text}'")
        print(f"   Processed: '{processed}'")
        return True
    except Exception as e:
        print(f"   Error: {e}")
        return False

def run_verification():
    """Run all verification checks"""
    print_header("AI CHATBOT - SYSTEM VERIFICATION")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'NLTK Data': check_nltk_data(),
        'Configuration': check_env_file(),
        'Training Data': check_intents_file(),
        'Database': check_database(),
        'ML Models': check_model_files(),
        'NLP Processing': test_nlp_processing()
    }
    
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    
    for check, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED! System is ready to run.")
        print("\n📝 Next steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Test the chatbot!")
    else:
        print("\n  Some checks failed. Please fix the issues above.")
        print("\n Common fixes:")
        print("  - Dependencies: pip install -r requirements.txt")
        print("  - NLTK Data: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')\"")
        print("  - Database: mysql -u root -p chatbot_db < database/schema.sql")
        print("  - ML Models: python train_model.py")
        print("  - Configuration: Copy .env.example to .env and update")
    
    print("\n" + "=" * 60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_verification()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n Unexpected error: {e}")
        sys.exit(1)
