# Complete Setup Guide - AI Chatbot Project

This guide will walk you through setting up the AI Chatbot project step-by-step.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important**: During installation, check "Add Python to PATH"

2. **MySQL Server 8.0+**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Remember the root password you set during installation

3. **Code Editor**
   - VS Code (Recommended): https://code.visualstudio.com/
   - Or any text editor of your choice

4. **Git** (Optional but recommended)
   - Download from: https://git-scm.com/downloads

---

## 🚀 Step-by-Step Installation

### Step 1: Extract/Clone the Project

```bash
# If you have the ZIP file:
# Extract it to: F:\PROJECT'S\Chatbot

# If using Git:
git clone <repository-url>
cd Chatbot
```

### Step 2: Open in VS Code

```bash
# Navigate to project directory
cd "F:\PROJECT'S\Chatbot"

# Open in VS Code
code .
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your terminal
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**Troubleshooting:**
- If `python` command doesn't work, try `python3` or `py`
- If activation fails, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` (Windows PowerShell)

### Step 4: Install Python Dependencies

```bash
# Make sure virtual environment is activated (you see (venv))
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**This will install:**
- Flask (Web framework)
- MySQL connector
- Scikit-learn (Machine Learning)
- NLTK (Natural Language Processing)
- SpeechRecognition (Voice input)
- pyttsx3 (Text-to-Speech)
- And more...

**If installation fails:**
```bash
# Try installing packages one by one
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install mysql-connector-python==8.2.0
# ... and so on
```

### Step 5: Download NLTK Data

```bash
# Run this command to download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

**Alternatively, run Python interactively:**
```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> nltk.download('wordnet')
>>> exit()
```

### Step 6: Setup MySQL Database

#### 6.1 Start MySQL Server

**Windows:**
- Open Services (Win + R, type `services.msc`)
- Find "MySQL80" service
- Right-click → Start

**macOS:**
```bash
mysql.server start
```

**Linux:**
```bash
sudo systemctl start mysql
```

#### 6.2 Login to MySQL

```bash
mysql -u root -p
# Enter your MySQL root password
```

#### 6.3 Create Database

```sql
-- Create the database
CREATE DATABASE chatbot_db;

-- Verify it was created
SHOW DATABASES;

-- Exit MySQL
EXIT;
```

#### 6.4 Import Database Schema

**Windows:**
```bash
mysql -u root -p chatbot_db < database\schema.sql
```

**macOS/Linux:**
```bash
mysql -u root -p chatbot_db < database/schema.sql
```

**Alternative method (if above doesn't work):**
```bash
# Login to MySQL
mysql -u root -p

# Use the database
USE chatbot_db;

# Copy and paste the contents of schema.sql file
# Or use:
SOURCE database/schema.sql;

EXIT;
```

#### 6.5 Verify Database Setup

```bash
mysql -u root -p chatbot_db

# Check tables
SHOW TABLES;
# You should see: admin_users, intents, responses, chat_logs

# Check sample data
SELECT COUNT(*) FROM intents;
# Should return 15

SELECT COUNT(*) FROM responses;
# Should return 60+

EXIT;
```

### Step 7: Configure Environment Variables

```bash
# Copy the example environment file
copy .env.example .env     # Windows
cp .env.example .env       # macOS/Linux
```

Edit the `.env` file with your details:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here  # ← Change this!
DB_NAME=chatbot_db

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here  # ← Change this!

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123  # ← Change this in production!

# Application Settings
PORT=5000
DEBUG=True
```

### Step 8: Train the Machine Learning Model

```bash
# Make sure virtual environment is activated
python train_model.py
```

**Expected Output:**
```
🤖 AI CHATBOT - INTENT CLASSIFICATION TRAINING
============================================================
📂 Loading training data from intents.json...
✓ Loaded 150+ patterns across 15 intents
🔄 Preprocessing text data...
✓ Preprocessed 150+ patterns
🤖 Training Intent Classification Model...
============================================================
📊 Intent Classes: 15
📚 Training samples: 120
📝 Testing samples: 30
🔢 Creating TF-IDF features...
✓ Feature dimensions: 500+
🎯 Training Logistic Regression classifier...
✓ Model training completed
============================================================
📊 MODEL EVALUATION RESULTS
============================================================
Accuracy:           0.9500 (95.00%)
Precision:          0.9480
Recall:             0.9500
F1-Score:           0.9490
Cross-Val Accuracy: 0.9400 (±0.0200)
============================================================
💾 Saving trained model...
✓ Saved classifier to models/intent_classifier.pkl
✓ Saved vectorizer to models/vectorizer.pkl
✓ Saved intent labels to models/intent_labels.pkl
✅ TRAINING COMPLETED SUCCESSFULLY!
```

**If you see errors:**
- Check that `intents.json` exists in the project root
- Ensure NLTK data is downloaded
- Verify all dependencies are installed

### Step 9: Run the Application

```bash
# Make sure virtual environment is activated
python app.py
```

**Expected Output:**
```
🤖 AI CHATBOT - STARTING SERVER
============================================================
✓ Model loaded successfully
✓ Connected to MySQL database: chatbot_db
✓ All systems ready!
============================================================
🌐 Server: http://localhost:5000
👤 Admin Panel: http://localhost:5000/admin
============================================================
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 10: Access the Application

Open your web browser and visit:

1. **Chatbot Interface**: http://localhost:5000
2. **Admin Panel**: http://localhost:5000/admin
3. **Admin Login**: http://localhost:5000/login

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed and added to PATH
- [ ] Virtual environment created and activated
- [ ] All Python packages installed successfully
- [ ] NLTK data downloaded
- [ ] MySQL server running
- [ ] Database `chatbot_db` created
- [ ] Database schema imported
- [ ] Sample data present in database
- [ ] `.env` file configured with correct credentials
- [ ] ML model trained successfully (models/*.pkl files exist)
- [ ] Flask application starts without errors
- [ ] Can access chatbot at http://localhost:5000
- [ ] Can login to admin panel
- [ ] Chatbot responds to test queries

---

## 🐛 Common Issues & Solutions

### Issue 1: "python: command not found"
**Solution:**
- Use `python3` or `py` instead
- Check if Python is added to PATH
- Reinstall Python and check "Add to PATH"

### Issue 2: "Access Denied" for MySQL
**Solution:**
- Check your MySQL password in `.env` file
- Ensure MySQL server is running
- Try resetting MySQL password

### Issue 3: "Module not found" errors
**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 4: Port 5000 already in use
**Solution:**
- Change PORT in `.env` to 5001 or another port
- Or stop the application using port 5000

### Issue 5: PyAudio installation fails
**Solution (Windows):**
```bash
# Download PyAudio wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Install it:
pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

### Issue 6: Voice input not working
**Solution:**
- Voice input requires Chrome or Edge browser
- Ensure microphone permissions are granted
- Check browser console for errors

### Issue 7: Model training fails
**Solution:**
- Ensure `intents.json` exists
- Check NLTK data is downloaded
- Verify sufficient disk space for model files

### Issue 8: Database connection fails
**Solution:**
```bash
# Test MySQL connection
mysql -u root -p

# Check if database exists
SHOW DATABASES;

# Verify credentials in .env file
```

---

## 🔄 Updating the Project

If you make changes to intents or responses:

1. **Update Database** (Admin Panel)
2. **Retrain Model** (Click "Retrain Model" button)
3. **Restart Server** (Ctrl+C, then `python app.py`)

---

## 🛑 Stopping the Application

```bash
# Press Ctrl+C in the terminal where app.py is running
# Deactivate virtual environment
deactivate
```

---

## 📚 Next Steps

1. **Test the Chatbot**: Try different queries
2. **Explore Admin Panel**: Add new intents and responses
3. **Customize**: Modify templates, colors, or responses
4. **Read VIVA_PREPARATION.md**: Prepare for project demonstration
5. **Read PROJECT_REPORT.md**: Understand the architecture

---

## 💡 Tips for Development

1. **Keep Virtual Environment Active**: Always activate before running
2. **Use Git**: Version control your changes
3. **Backup Database**: Export before making major changes
4. **Test Regularly**: Test after each new intent/response
5. **Check Logs**: Monitor terminal output for errors
6. **Document Changes**: Keep track of modifications

---

## 📞 Support

If you encounter issues:
1. Check error messages in terminal
2. Review this guide's troubleshooting section
3. Check MySQL and Flask logs
4. Verify all prerequisites are met
5. Ensure all files are in correct locations

---

**Congratulations! Your AI Chatbot is now running! 🎉**
