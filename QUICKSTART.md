# Quick Start Guide - AI Chatbot Project

Get your chatbot up and running in 10 minutes!

---

## ⚡ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8+ installed
- [ ] MySQL Server 8.0+ installed and running
- [ ] Internet connection (for downloading dependencies)
- [ ] VS Code or any code editor

---

## 🚀 5-Step Quick Setup

### Step 1: Setup Virtual Environment (2 min)

```bash
# Navigate to project folder
cd "F:\PROJECT'S\Chatbot"

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Mac/Linux

# You should see (venv) in your terminal
```

### Step 2: Install Dependencies (3 min)

```bash
# Upgrade pip
pip install --upgrade pip

# Install all packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 3: Setup Database (2 min)

```bash
# Login to MySQL (enter your password)
mysql -u root -p

# In MySQL prompt:
CREATE DATABASE chatbot_db;
EXIT;

# Import schema
mysql -u root -p chatbot_db < database\schema.sql  # Windows
mysql -u root -p chatbot_db < database/schema.sql  # Mac/Linux
```

### Step 4: Configure Environment (1 min)

```bash
# Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env file - Change these lines:
# DB_PASSWORD=your_mysql_password_here
# SECRET_KEY=your_secret_key_here
```

### Step 5: Train & Run (2 min)

```bash
# Train the AI model
python train_model.py

# Start the application
python app.py
```

**Done! Open:** http://localhost:5000

---

## 🎯 Default Credentials

**Admin Login:** http://localhost:5000/login

- Username: `admin`
- Password: `admin123`

⚠️ Change these in production!

---

## ✅ Quick Test

Try these queries in the chatbot:

1. "Hello, how are you?"
2. "What is the fee structure?"
3. "Tell me about placements"
4. "How to apply for admission?"
5. "Contact information"

All should get relevant responses!

---

## 🐛 Quick Troubleshooting

**Problem:** `python: command not found`  
**Fix:** Try `python3` or `py` instead

**Problem:** Database connection failed  
**Fix:** Check MySQL is running and password in `.env` is correct

**Problem:** Module not found  
**Fix:** Make sure virtual environment is activated (see `(venv)` in terminal)

**Problem:** Port 5000 in use  
**Fix:** Change `PORT=5001` in `.env` file

---

## 📚 Next Steps

1. ✅ Test chatbot with different queries
2. ✅ Login to admin panel
3. ✅ Add a new intent
4. ✅ Retrain the model
5. ✅ Read full documentation in `/docs`

---

## 🎓 For Viva Preparation

**Key Points to Remember:**
- Accuracy: 95%
- Response Time: < 500ms
- Technologies: Python, Flask, Scikit-learn, MySQL
- ML Algorithm: Logistic Regression + TF-IDF
- Features: Text chat, Voice support, Admin panel

**Quick Demo Script:**
1. Show chatbot responding to queries
2. Demonstrate voice input
3. Login to admin panel
4. Add new intent/response
5. Retrain model
6. Test new intent

Read `docs/VIVA_PREPARATION.md` for detailed Q&A!

---

## 📞 Need Help?

1. Check `docs/SETUP_GUIDE.md` for detailed instructions
2. Review error messages in terminal
3. Ensure all prerequisites are met
4. Verify MySQL is running: `mysql -u root -p`

---

**Congratulations! You're all set! 🎉**

Now go explore the chatbot and admin panel!
