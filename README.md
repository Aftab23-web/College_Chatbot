# 🤖 AI-Based Chatbot for College/Company Support

**A Final-Year Computer Science Project**

An intelligent chatbot system with NLP-powered intent classification, voice support, admin training panel, and MySQL database integration.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [AI/ML Logic Explanation](#aiml-logic-explanation)
- [Future Enhancements](#future-enhancements)
- [Academic Disclaimer](#academic-disclaimer)

---

## ✨ Features

### Core Functionality
- 💬 **Text-based Chat**: Type queries and get intelligent responses
- 🎤 **Voice Support**: Speech-to-Text input and Text-to-Speech output
- 🤖 **Intent Classification**: AI-powered understanding using NLP
- 📊 **Admin Panel**: Train and manage the chatbot
- 💾 **Database Integration**: MySQL for persistent storage
- 📝 **Chat Logging**: Track all conversations

### AI/ML Capabilities
- TF-IDF vectorization for text representation
- Logistic Regression for intent classification
- Confidence-based response selection
- Fallback handling for unknown queries
- NLP preprocessing (tokenization, lemmatization, stop-word removal)

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- Flask (Web Framework)
- MySQL (Database)

**AI/NLP:**
- Scikit-learn (Machine Learning)
- NLTK (Natural Language Processing)
- spaCy (Advanced NLP)

**Voice:**
- SpeechRecognition (Speech-to-Text)
- pyttsx3 (Text-to-Speech)

**Frontend:**
- HTML5
- Tailwind CSS
- Vanilla JavaScript

---

## 📁 Project Structure

```
Chatbot/
├── app.py                      # Main Flask application
├── train_model.py              # ML training script
├── intents.json                # Training dataset
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── database/
│   └── schema.sql              # MySQL database schema
├── models/
│   ├── intent_classifier.pkl   # Trained model (generated)
│   └── vectorizer.pkl          # TF-IDF vectorizer (generated)
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   └── js/
│       ├── chat.js             # Chat interface logic
│       └── admin.js            # Admin panel logic
├── templates/
│   ├── index.html              # Main chatbot interface
│   ├── admin.html              # Admin panel
│   └── login.html              # Admin login
├── utils/
│   ├── __init__.py
│   ├── nlp_processor.py        # NLP preprocessing
│   └── db_manager.py           # Database operations
└── docs/
    ├── SETUP_GUIDE.md          # Detailed setup instructions
    ├── VIVA_PREPARATION.md     # Viva Q&A guide
    └── PROJECT_REPORT.md       # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- pip (Python package manager)
- Git (optional)

### Step 1: Clone/Download Project
```bash
# If using Git
git clone <repository-url>
cd Chatbot

# Or simply extract the ZIP file
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 5: Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE chatbot_db;
exit;

# Import schema
mysql -u root -p chatbot_db < database/schema.sql
```

### Step 6: Configure Environment
```bash
# Copy .env.example to .env
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env file with your database credentials
```

### Step 7: Train the Model
```bash
python train_model.py
```

---

## ▶️ How to Run

### Start the Application
```bash
python app.py
```

The application will be available at:
- **Chatbot Interface**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Admin Login**: http://localhost:5000/login

### Default Admin Credentials
- **Username**: admin
- **Password**: admin123

⚠️ **Change these credentials in production!**

---

## 📖 Usage Guide

### For End Users
1. Open http://localhost:5000
2. Type your query or use the microphone button for voice input
3. Get instant AI-powered responses
4. Chat history is maintained in the session

### For Administrators
1. Login at http://localhost:5000/login
2. **Add New Intent**: Create new question patterns
3. **Manage Responses**: Update bot responses
4. **Retrain Model**: Apply changes and retrain AI
5. **View Logs**: Monitor chat conversations

---

## 🧠 AI/ML Logic Explanation

### Why Intent Classification?
Intent classification is chosen because:
- **Structured Responses**: FAQs have predefined categories
- **Fast & Efficient**: Lightweight model suitable for local deployment
- **Explainable**: Easy to understand and demonstrate in viva
- **Training-friendly**: Can be retrained without GPU

### NLP Approach

#### 1. **Text Preprocessing**
```python
Text → Tokenization → Stop Word Removal → Lemmatization → Clean Text
```

#### 2. **Feature Extraction**
- **TF-IDF Vectorization**: Converts text to numerical features
- Captures word importance across documents
- Creates sparse matrix representation

#### 3. **Classification Model**
- **Logistic Regression**: Multi-class classification
- Probability-based predictions (confidence scores)
- Fast training and inference

#### 4. **Response Selection**
```python
if confidence > 0.6:
    return matched_response
else:
    return fallback_response
```

### Model Evaluation
- **Accuracy**: Overall correctness
- **Precision**: Correct positive predictions
- **Recall**: Coverage of actual positives
- **F1-Score**: Harmonic mean of precision & recall
- **Confusion Matrix**: Detailed performance analysis

### Training Pipeline
```
intents.json → Preprocessing → TF-IDF → Logistic Regression → Save Model
```

---

## 🚀 Future Enhancements

1. **GPT Integration**
   - Use OpenAI API for more natural responses
   - Hybrid approach: Intent classification + GPT fallback

2. **Multilingual Support**
   - Add Hindi, Tamil, or other regional languages
   - Use language detection

3. **Sentiment Analysis**
   - Detect user frustration
   - Route to human agents when needed

4. **Cloud Deployment**
   - Deploy on AWS/Azure/Heroku
   - Use cloud databases (RDS)

5. **Mobile Application**
   - React Native or Flutter app
   - Push notifications

6. **Analytics Dashboard**
   - User engagement metrics
   - Popular queries visualization
   - Performance monitoring

7. **Advanced NLP**
   - BERT/Transformer models
   - Entity recognition (dates, names, etc.)
   - Context-aware conversations

---

## 📚 Academic Disclaimer

This project is developed for educational purposes as part of a Computer Science final-year project. It demonstrates:
- Software engineering principles
- AI/ML implementation
- Full-stack development
- Database management

**Note**: For production deployment, additional security measures, error handling, and scalability considerations are required.

---

## 📄 License

This project is for academic use only. Feel free to modify and extend for your learning purposes.

---

## 👨‍💻 Author

**Computer Science Final Year Project**  
Year: 2025-2026

---

## 🤝 Support

For issues or questions:
1. Check the documentation in `/docs` folder
2. Review `VIVA_PREPARATION.md` for common questions
3. Refer to `SETUP_GUIDE.md` for troubleshooting

---

**Happy Coding! 🚀**
