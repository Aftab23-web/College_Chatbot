"""
AI Chatbot Flask Application
Main backend server with chat, admin, and voice support
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os
import json
import pickle
import random
from datetime import datetime
from dotenv import load_dotenv
import uuid

# Voice support (optional)
voice_support_available = False
sr = None
pyttsx3 = None
try:
    import speech_recognition as sr
    import pyttsx3
    voice_support_available = True
    print("✓ Voice support enabled")
except Exception as e:
    print(f"⚠ Voice support disabled: {e}")
    sr = None
    pyttsx3 = None

# Custom modules
from utils.nlp_processor import NLPProcessor
from utils.db_manager import DatabaseManager

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
CORS(app)

# Configuration
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'
CONFIDENCE_THRESHOLD = 0.15  # Minimum confidence for intent matching (lowered for better responses)

# Initialize components
print("Initializing components...")
try:
    db_manager = DatabaseManager()
    print("✓ Database manager initialized")
except Exception as e:
    print(f"⚠ Database manager initialization warning: {e}")
    db_manager = None

try:
    nlp_processor = NLPProcessor()
    print("✓ NLP processor initialized")
except Exception as e:
    print(f"✗ Error initializing NLP processor: {e}")
    nlp_processor = None

# Load trained model
MODEL_DIR = 'models'
vectorizer = None
classifier = None
intent_labels = []

def load_model():
    """Load trained ML model"""
    global vectorizer, classifier, intent_labels
    
    try:
        with open(os.path.join(MODEL_DIR, 'vectorizer.pkl'), 'rb') as f:
            vectorizer = pickle.load(f)
        
        with open(os.path.join(MODEL_DIR, 'intent_classifier.pkl'), 'rb') as f:
            classifier = pickle.load(f)
        
        with open(os.path.join(MODEL_DIR, 'intent_labels.pkl'), 'rb') as f:
            intent_labels = pickle.load(f)
        
        print("✓ Model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        print("⚠️  Please run train_model.py first")
        return False

# Load intents from JSON
def load_intents():
    """Load intents from intents.json"""
    try:
        with open('intents.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"✗ Error loading intents: {e}")
        return {"intents": []}

intents_data = load_intents()

# ==================== HELPER FUNCTIONS ====================

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def predict_intent(user_message):
    """
    Predict intent and return response
    
    Args:
        user_message (str): User's input message
        
    Returns:
        dict: Response with intent, confidence, and message
    """
    # Check if NLP processor is available
    if nlp_processor is None:
        return {
            'intent': 'error',
            'confidence': 0.0,
            'response': 'Sorry, the chatbot is not properly initialized. Please contact support.'
        }
    
    # Check if model is loaded
    if vectorizer is None or classifier is None:
        return {
            'intent': 'error',
            'confidence': 0.0,
            'response': 'Sorry, the AI model is not loaded. Please contact support.'
        }
    
    try:
        # Preprocess message
        processed_message = nlp_processor.preprocess(user_message)
        
        # Vectorize
        message_tfidf = vectorizer.transform([processed_message])
        
        # Predict intent
        predicted_intent = classifier.predict(message_tfidf)[0]
        
        # Get confidence
        probabilities = classifier.predict_proba(message_tfidf)[0]
        confidence = max(probabilities)
        
        # Get response
        if confidence >= CONFIDENCE_THRESHOLD:
            response_text = get_response_for_intent(predicted_intent)
        else:
            predicted_intent = 'unknown'
            response_text = get_fallback_response()
        
        return {
            'intent': predicted_intent,
            'confidence': float(confidence),
            'response': response_text
        }
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'intent': 'error',
            'confidence': 0.0,
            'response': 'Sorry, I encountered an error processing your message. Please try again.'
        }

def get_response_for_intent(intent_tag):
    """Get random response for an intent"""
    # Debug: Print current intents_data state
    total_intents = len(intents_data.get('intents', []))
    print(f"🔍 Looking for intent '{intent_tag}' in {total_intents} loaded intents")
    
    for intent in intents_data['intents']:
        if intent['tag'] == intent_tag:
            responses = intent.get('responses', [])
            if responses:
                print(f"✓ Found {len(responses)} responses for intent '{intent_tag}'")
                return random.choice(responses)
            else:
                print(f"⚠ Intent '{intent_tag}' has no responses!")
    
    print(f"⚠ Intent '{intent_tag}' not found in intents_data!")
    return get_fallback_response()

def get_fallback_response():
    """Return fallback response for unknown queries"""
    fallback_messages = [
        "I'm sorry, I didn't quite understand that. Could you please rephrase your question?",
        "I'm not sure about that. You can ask about admissions, courses, fees, placements, or facilities.",
        "I couldn't find an answer to that. Please try asking in a different way or contact our support team.",
        "That's a bit unclear to me. Can you provide more details or ask about something else?"
    ]
    return random.choice(fallback_messages)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('index.html')

@app.route('/api/check-login', methods=['GET'])
def check_login():
    """Check if user is logged in"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'id': session['user_id'],
                'username': session.get('username', 'User')
            }
        })
    return jsonify({'logged_in': False})

@app.route('/api/user-register', methods=['POST'])
def user_register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if db_manager.connect():
            # Hash password
            import bcrypt
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user
            query = "INSERT INTO users (username, password_hash, full_name, email) VALUES (%s, %s, %s, %s)"
            try:
                db_manager.execute_query(query, (username, password_hash, full_name, email))
                db_manager.disconnect()
                return jsonify({'success': True, 'message': 'Registration successful'})
            except Exception as e:
                db_manager.disconnect()
                if 'Duplicate entry' in str(e):
                    return jsonify({'error': 'Username already exists'}), 400
                return jsonify({'error': 'Registration failed'}), 500
        
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-login', methods=['POST'])
def user_login():
    """User login - also checks for admin credentials"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if db_manager.connect():
            # First check if it's an admin
            admin = db_manager.verify_admin(username, password)
            
            if admin:
                # Set admin session
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                session['is_admin'] = True
                db_manager.disconnect()
                
                return jsonify({
                    'success': True,
                    'isAdmin': True,
                    'user': {
                        'id': admin['id'],
                        'username': admin['username']
                    }
                })
            
            # If not admin, check regular users
            query = "SELECT id, username, password_hash, full_name FROM users WHERE username = %s AND is_active = TRUE"
            users = db_manager.execute_query(query, (username,), fetch=True)
            db_manager.disconnect()
            
            if users and len(users) > 0:
                user = users[0]
                import bcrypt
                
                if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    # Update last login
                    if db_manager.connect():
                        db_manager.execute_query("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
                        db_manager.disconnect()
                    
                    # Set session
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['is_admin'] = False
                    
                    return jsonify({
                        'success': True,
                        'isAdmin': False,
                        'user': {
                            'id': user['id'],
                            'username': user['username'],
                            'full_name': user.get('full_name', '')
                        }
                    })
            
            return jsonify({'error': 'Invalid username or password'}), 401
        
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-logout', methods=['POST'])
def user_logout():
    """User logout"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    return jsonify({'success': True})

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    
    Request JSON:
        {
            "message": "user message"
        }
    
    Response JSON:
        {
            "response": "bot response",
            "intent": "predicted_intent",
            "confidence": 0.85
        }
    """
    try:
        # Check if user is logged in
        if 'user_id' not in session:
            return jsonify({'error': 'Please login to chat'}), 401
        
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Predict intent and get response
        result = predict_intent(user_message)
        
        # Log conversation with user_id
        session_id = get_session_id()
        user_ip = request.remote_addr
        user_id = session.get('user_id')
        
        if db_manager.connect():
            db_manager.log_chat(
                user_message=user_message,
                bot_response=result['response'],
                predicted_intent=result['intent'],
                confidence_score=result['confidence'],
                session_id=session_id,
                user_ip=user_ip,
                user_id=user_id
            )
            db_manager.disconnect()
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'An error occurred'}), 500
        return jsonify({
            'error': 'An error occurred',
            'response': 'Sorry, I encountered an error. Please try again.'
        }), 500

@app.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    """
    Convert speech to text
    
    Response JSON:
        {
            "text": "recognized text"
        }
    """
    if not voice_support_available:
        return jsonify({'error': 'Voice support not available in Python 3.13+'}), 503
    
    try:
        recognizer = sr.Recognizer()
        
        # Check if audio file is uploaded
        if 'audio' in request.files:
            audio_file = request.files['audio']
            
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                return jsonify({'text': text})
        
        # Use microphone
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
            
            text = recognizer.recognize_google(audio)
            return jsonify({'text': text})
    
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Convert text to speech
    
    Request JSON:
        {
            "text": "text to speak"
        }
    
    Note: This triggers audio on server side. 
    For production, use client-side TTS or return audio file.
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Initialize TTS engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed
        engine.setProperty('volume', 0.9)  # Volume
        
        # Speak (server-side - consider client-side for production)
        engine.say(text)
        engine.runAndWait()
        
        return jsonify({'success': True, 'message': 'Speech generated'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ADMIN ROUTES ====================

@app.route('/api/admin/login', methods=['POST'])
def admin_login_api():
    """Admin login API endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password are required'}), 400
    
    if db_manager.connect():
        admin = db_manager.verify_admin(username, password)
        db_manager.disconnect()
        
        if admin:
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'success': False, 'error': 'Database connection error'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login - redirect to home page (login now handled via modal)"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if db_manager.connect():
            admin = db_manager.verify_admin(username, password)
            db_manager.disconnect()
            
            if admin:
                session['admin_id'] = admin['id']
                session['admin_username'] = admin['username']
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    
    # Redirect GET requests to home page
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    """Admin panel"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('admin.html', username=session.get('admin_username'))

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get all intents"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if db_manager.connect():
        intents = db_manager.get_all_intents()
        db_manager.disconnect()
        return jsonify(intents)
    
    return jsonify({'error': 'Database error'}), 500

@app.route('/api/intents', methods=['POST'])
def add_intent():
    """Add new intent"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    intent_name = data.get('intent_name')
    description = data.get('description', '')
    
    if db_manager.connect():
        success = db_manager.add_intent(intent_name, description)
        db_manager.disconnect()
        
        if success:
            return jsonify({'success': True, 'message': 'Intent added'})
    
    return jsonify({'error': 'Failed to add intent'}), 500

@app.route('/api/responses/<int:intent_id>', methods=['GET'])
def get_responses(intent_id):
    """Get responses for an intent"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if db_manager.connect():
        responses = db_manager.get_responses_by_intent(intent_id)
        db_manager.disconnect()
        return jsonify(responses)
    
    return jsonify({'error': 'Database error'}), 500

@app.route('/api/responses', methods=['POST'])
def add_response():
    """Add new response"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    intent_id = data.get('intent_id')
    pattern = data.get('pattern')
    response = data.get('response')
    priority = data.get('priority', 0)
    
    if db_manager.connect():
        success = db_manager.add_response(intent_id, pattern, response, priority)
        db_manager.disconnect()
        
        if success:
            return jsonify({'success': True, 'message': 'Response added'})
    
    return jsonify({'error': 'Failed to add response'}), 500

@app.route('/api/responses/<int:response_id>', methods=['DELETE'])
def delete_response(response_id):
    """Delete a response"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    if db_manager.connect():
        success = db_manager.delete_response(response_id)
        db_manager.disconnect()
        
        if success:
            return jsonify({'success': True, 'message': 'Response deleted'})
    
    return jsonify({'error': 'Failed to delete response'}), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Retrain the model with updated data"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        print("\n" + "="*60)
        print("Starting model retraining...")
        print("="*60)
        
        # Export training data from database
        if db_manager.connect():
            print("✓ Connected to database")
            training_data = db_manager.export_training_data()
            db_manager.disconnect()
            
            num_intents = len(training_data.get('intents', []))
            print(f"✓ Exported {num_intents} intents")
            
            # Validate training data
            if num_intents == 0:
                print("✗ No valid intents found for training!")
                print("="*60 + "\n")
                return jsonify({
                    'error': 'No valid intents found',
                    'details': 'Please add intents with both patterns and responses before retraining.'
                }), 400
            
            # Save to intents.json
            with open('intents.json', 'w', encoding='utf-8') as f:
                json.dump(training_data, f, indent=2, ensure_ascii=False)
            print("✓ Saved to intents.json")
            
            # Verify the saved file
            with open('intents.json', 'r', encoding='utf-8') as f:
                verify_data = json.load(f)
                print(f"✓ Verified intents.json: {len(verify_data.get('intents', []))} intents")
            
            # Run training script
            import subprocess
            import sys
            
            # Use the same Python executable that's running this app
            python_exe = sys.executable
            print(f"✓ Running training with: {python_exe}")
            
            result = subprocess.run([python_exe, 'train_model.py'], 
                                  capture_output=True, 
                                  text=True,
                                  cwd=os.path.dirname(os.path.abspath(__file__)))
            
            print(f"Training exit code: {result.returncode}")
            if result.stdout:
                print("STDOUT:", result.stdout[-500:])  # Last 500 chars
            if result.stderr:
                print("STDERR:", result.stderr[-500:])  # Last 500 chars
            
            if result.returncode == 0:
                # Reload model and intents
                global vectorizer, classifier, intent_labels, intents_data
                print("✓ Reloading model...")
                
                # Reload the model files
                model_loaded = load_model()
                
                if model_loaded:
                    # Reload intents.json into global variable
                    intents_data = load_intents()
                    print(f"✓ Reloaded {len(intents_data.get('intents', []))} intents into memory")
                    
                    # Verify the model can make predictions
                    try:
                        test_message = "hello"
                        processed = nlp_processor.preprocess(test_message)
                        test_vector = vectorizer.transform([processed])
                        test_pred = classifier.predict(test_vector)
                        print(f"✓ Model verification successful - test prediction: {test_pred[0]}")
                    except Exception as verify_error:
                        print(f"⚠ Model verification warning: {verify_error}")
                    
                    print("="*60)
                    print("✓ Model retrained and reloaded successfully!")
                    print("="*60 + "\n")
                    return jsonify({
                        'success': True, 
                        'message': f'Model retrained successfully! Loaded {num_intents} intents. The chatbot is now updated.'
                    })
                else:
                    print("✗ Model reload failed!")
                    print("="*60 + "\n")
                    return jsonify({
                        'error': 'Model trained but reload failed',
                        'details': 'The training succeeded but the model could not be loaded. Please restart the application.'
                    }), 500
            else:
                print("✗ Training failed!")
                print("="*60 + "\n")
                return jsonify({
                    'error': 'Training failed',
                    'details': result.stderr or result.stdout
                }), 500
        
        return jsonify({'error': 'Database connection failed'}), 500
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"✗ Retrain error: {e}")
        print(error_details)
        return jsonify({'error': str(e), 'details': error_details}), 500

@app.route('/api/chat-logs', methods=['GET'])
def get_chat_logs():
    """Get recent chat logs"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    limit = request.args.get('limit', 100, type=int)
    
    if db_manager.connect():
        logs = db_manager.get_chat_logs(limit)
        db_manager.disconnect()
        
        # Convert datetime to string
        for log in logs:
            if log.get('created_at'):
                log['created_at'] = log['created_at'].isoformat()
        
        return jsonify(logs)
    
    return jsonify({'error': 'Database error'}), 500

@app.route('/api/debug/model-status', methods=['GET'])
def debug_model_status():
    """Debug endpoint to check model and intents status"""
    if 'admin_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        status = {
            'model_loaded': vectorizer is not None and classifier is not None,
            'nlp_processor_available': nlp_processor is not None,
            'intents_loaded': len(intents_data.get('intents', [])),
            'intent_labels': intent_labels if intent_labels else [],
            'intents_list': [intent['tag'] for intent in intents_data.get('intents', [])]
        }
        
        # Try to read intents.json directly
        try:
            with open('intents.json', 'r', encoding='utf-8') as f:
                file_data = json.load(f)
                status['intents_json_file_count'] = len(file_data.get('intents', []))
        except Exception as e:
            status['intents_json_error'] = str(e)
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🤖 VIKAS COLLEGE CHATBOT - STARTING SERVER")
    print("=" * 60)
    
    # Load model
    model_loaded = load_model()
    
    if not model_loaded:
        print("\n⚠️  WARNING: Model not loaded!")
        print("Please run: python train_model.py")
        print("=" * 60 + "\n")
    else:
        print("\n✓ All systems ready!")
        print("=" * 60)
        print(f"🌐 Server: http://localhost:{os.getenv('PORT', 5000)}")
        print(f"👤 Admin Panel: http://localhost:{os.getenv('PORT', 5000)}/admin")
        print("=" * 60 + "\n")
        
        # Run Flask app
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=app.config['DEBUG']
        )
