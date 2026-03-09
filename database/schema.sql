-- ============================================
-- AI Chatbot Database Schema
-- Database: chatbot_db
-- ============================================

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS chat_logs;
DROP TABLE IF EXISTS responses;
DROP TABLE IF EXISTS intents;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin_users;

-- ============================================
-- Table: admin_users
-- Stores admin credentials for the training panel
-- ============================================
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: users
-- Stores regular user credentials for chat access
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: intents
-- Stores intent categories for classification
-- ============================================
CREATE TABLE intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intent_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: responses
-- Stores patterns and responses for each intent
-- ============================================
CREATE TABLE responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intent_id INT NOT NULL,
    pattern TEXT NOT NULL,
    response TEXT NOT NULL,
    priority INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
    INDEX idx_intent_id (intent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Table: chat_logs
-- Stores all chat conversations for analytics
-- ============================================
CREATE TABLE chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    predicted_intent VARCHAR(100),
    confidence_score FLOAT,
    session_id VARCHAR(100),
    user_ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at),
    INDEX idx_predicted_intent (predicted_intent)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- Insert Default Admin User
-- Username: admin, Password: admin123 (hashed with bcrypt)
-- ⚠️ CHANGE THIS IN PRODUCTION!
-- ============================================
INSERT INTO admin_users (username, password_hash, email) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ7LXu', 'admin@chatbot.local');

-- ============================================
-- Insert Sample Intents
-- ============================================
INSERT INTO intents (intent_name, description) VALUES
('greeting', 'User greets the chatbot'),
('goodbye', 'User says goodbye'),
('thanks', 'User expresses gratitude'),
('about', 'Questions about the institution/company'),
('admission', 'Admission-related queries'),
('fees', 'Fee structure and payment queries'),
('courses', 'Available courses/programs'),
('placement', 'Placement and career support'),
('hostel', 'Hostel and accommodation'),
('library', 'Library facilities'),
('contact', 'Contact information'),
('timings', 'Working hours and schedules'),
('leave_policy', 'Leave and attendance policy'),
('help', 'General help requests'),
('unknown', 'Fallback for unknown queries');

-- ============================================
-- Insert Sample Responses and Patterns
-- ============================================

-- Greeting Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'greeting'), 'hello', 'Hello! How can I assist you today?'),
((SELECT id FROM intents WHERE intent_name = 'greeting'), 'hi', 'Hi there! Welcome to our support chatbot. How may I help you?'),
((SELECT id FROM intents WHERE intent_name = 'greeting'), 'hey', 'Hey! What can I do for you today?'),
((SELECT id FROM intents WHERE intent_name = 'greeting'), 'good morning', 'Good morning! How can I help you?'),
((SELECT id FROM intents WHERE intent_name = 'greeting'), 'good evening', 'Good evening! What brings you here today?');

-- Goodbye Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'goodbye'), 'bye', 'Goodbye! Have a great day!'),
((SELECT id FROM intents WHERE intent_name = 'goodbye'), 'see you', 'See you later! Feel free to return if you have more questions.'),
((SELECT id FROM intents WHERE intent_name = 'goodbye'), 'goodbye', 'Goodbye! Take care and feel free to reach out anytime.'),
((SELECT id FROM intents WHERE intent_name = 'goodbye'), 'take care', 'Take care! We''re always here to help.');

-- Thanks Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'thanks'), 'thank you', 'You''re welcome! Happy to help!'),
((SELECT id FROM intents WHERE intent_name = 'thanks'), 'thanks', 'You''re welcome! Let me know if you need anything else.'),
((SELECT id FROM intents WHERE intent_name = 'thanks'), 'appreciate it', 'Glad I could help! Feel free to ask more questions.'),
((SELECT id FROM intents WHERE intent_name = 'thanks'), 'thanks a lot', 'You''re very welcome! Have a great day!');

-- About Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'about'), 'what is this college about', 'We are a premier institution offering quality education in Engineering, Management, and Sciences. Established in 2000, we focus on academic excellence and holistic development.'),
((SELECT id FROM intents WHERE intent_name = 'about'), 'tell me about your institution', 'Our institution is dedicated to providing world-class education with state-of-the-art facilities, experienced faculty, and strong industry connections.'),
((SELECT id FROM intents WHERE intent_name = 'about'), 'company information', 'We are a leading organization committed to innovation and excellence. Our mission is to deliver quality services while fostering growth and development.');

-- Admission Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'admission'), 'how to apply for admission', 'You can apply online through our website. Visit the Admissions section, fill out the application form, and submit the required documents. Admissions are open from May to July.'),
((SELECT id FROM intents WHERE intent_name = 'admission'), 'admission process', 'The admission process includes: 1) Online application, 2) Document submission, 3) Entrance test (if applicable), 4) Interview, 5) Final selection and fee payment.'),
((SELECT id FROM intents WHERE intent_name = 'admission'), 'when do admissions open', 'Admissions typically open in May and close in July. Please check our website for exact dates and deadlines.'),
((SELECT id FROM intents WHERE intent_name = 'admission'), 'eligibility criteria', 'Eligibility varies by program. Generally, you need 10+2 for undergraduate and a relevant bachelor''s degree for postgraduate programs. Check specific program requirements on our website.');

-- Fees Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'fees'), 'what is the fee structure', 'Fee structure varies by program. Undergraduate courses: ₹80,000-₹1,20,000 per year. Postgraduate courses: ₹60,000-₹1,00,000 per year. Hostel fees are additional.'),
((SELECT id FROM intents WHERE intent_name = 'fees'), 'how much are the fees', 'Annual fees range from ₹80,000 to ₹1,20,000 depending on the course. Contact the accounts department for detailed breakdown.'),
((SELECT id FROM intents WHERE intent_name = 'fees'), 'payment options', 'We accept payment through online transfer, debit/credit cards, demand drafts, and installments. You can pay in 2-3 installments per semester.'),
((SELECT id FROM intents WHERE intent_name = 'fees'), 'scholarship available', 'Yes! We offer merit-based and need-based scholarships. Eligible students can receive 10-50% fee waiver. Apply during admission or contact the scholarship office.');

-- Courses Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'courses'), 'what courses do you offer', 'We offer B.Tech (CSE, ECE, Mechanical, Civil), MBA, MCA, M.Tech, and various diploma programs. Check our website for the complete list.'),
((SELECT id FROM intents WHERE intent_name = 'courses'), 'available programs', 'Available programs include Engineering, Management, Computer Applications, and Sciences at undergraduate and postgraduate levels.'),
((SELECT id FROM intents WHERE intent_name = 'courses'), 'computer science course', 'We offer B.Tech in Computer Science & Engineering (4 years) and MCA (2 years). Both programs include AI, ML, Web Development, and other modern technologies.');

-- Placement Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'placement'), 'placement record', 'Our placement record is excellent! 85% of students get placed with an average package of ₹4.5 LPA. Top packages reach ₹12-15 LPA.'),
((SELECT id FROM intents WHERE intent_name = 'placement'), 'top recruiters', 'Top recruiters include TCS, Infosys, Wipro, Cognizant, Amazon, Microsoft, and many startups. We have 200+ partner companies.'),
((SELECT id FROM intents WHERE intent_name = 'placement'), 'placement training', 'Yes! We provide comprehensive placement training including aptitude, technical skills, communication, and interview preparation from the 3rd year onwards.'),
((SELECT id FROM intents WHERE intent_name = 'placement'), 'internship opportunities', 'We facilitate internships in leading companies. Students can do summer internships after 2nd/3rd year. Many internships convert to full-time offers.');

-- Hostel Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'hostel'), 'hostel facilities', 'We have separate boys and girls hostels with 24/7 security, WiFi, mess facilities, gym, and recreation rooms. Rooms are available in 2-3 sharing options.'),
((SELECT id FROM intents WHERE intent_name = 'hostel'), 'hostel fees', 'Hostel fees are approximately ₹60,000-₹80,000 per year including accommodation and food. AC rooms are available at higher rates.'),
((SELECT id FROM intents WHERE intent_name = 'hostel'), 'hostel availability', 'Hostel accommodation is available on first-come-first-served basis. Apply during admission. Contact the hostel warden for availability.');

-- Library Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'library'), 'library timings', 'The library is open from 8:00 AM to 8:00 PM on weekdays and 9:00 AM to 5:00 PM on weekends. During exams, extended hours till 10:00 PM are available.'),
((SELECT id FROM intents WHERE intent_name = 'library'), 'library facilities', 'Our library has 50,000+ books, e-journals, digital resources, study rooms, computer terminals, and a peaceful reading environment.'),
((SELECT id FROM intents WHERE intent_name = 'library'), 'book borrowing', 'Students can borrow up to 3 books for 15 days. Renewal is possible if no other requests are pending. Late returns incur a small fine.');

-- Contact Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'contact'), 'contact information', 'You can reach us at: Phone: +91-123-456-7890, Email: info@college.edu, Website: www.college.edu. Office hours: 9 AM - 5 PM (Mon-Sat)'),
((SELECT id FROM intents WHERE intent_name = 'contact'), 'email address', 'Our official email is info@college.edu. For admissions, contact admissions@college.edu. For technical support, reach support@college.edu.'),
((SELECT id FROM intents WHERE intent_name = 'contact'), 'phone number', 'Contact us at +91-123-456-7890 (Main office) or +91-123-456-7891 (Admissions). We''re available Monday to Saturday, 9 AM to 5 PM.');

-- Timings Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'timings'), 'office timings', 'Office timings: Monday to Saturday, 9:00 AM to 5:00 PM. Closed on Sundays and public holidays.'),
((SELECT id FROM intents WHERE intent_name = 'timings'), 'class timings', 'Classes run from 9:00 AM to 4:00 PM with breaks. Exact schedule varies by program and semester. Check your timetable for details.'),
((SELECT id FROM intents WHERE intent_name = 'timings'), 'working hours', 'We operate Monday to Saturday, 9:00 AM to 5:00 PM. For urgent matters, contact the 24/7 helpline: +91-123-456-7890.');

-- Leave Policy Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'leave_policy'), 'leave policy', 'Students must maintain 75% attendance. Leave requires prior approval and valid documentation. Medical leaves need doctor''s certificate.'),
((SELECT id FROM intents WHERE intent_name = 'leave_policy'), 'attendance requirement', 'Minimum 75% attendance is mandatory. Below this, you may not be eligible for exams. Genuine cases are considered with proper documentation.'),
((SELECT id FROM intents WHERE intent_name = 'leave_policy'), 'sick leave', 'For sick leave, submit a medical certificate to your department within 3 days. Prolonged illness requires approval from the Dean.');

-- Help Intent
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'help'), 'i need help', 'I''m here to help! You can ask me about admissions, fees, courses, placements, facilities, or any other queries. What would you like to know?'),
((SELECT id FROM intents WHERE intent_name = 'help'), 'what can you do', 'I can help you with information about admissions, courses, fees, placements, hostel, library, contact details, and general queries. Just ask away!'),
((SELECT id FROM intents WHERE intent_name = 'help'), 'how do you work', 'I use AI to understand your questions and provide relevant answers. I''m trained on college/company information. Ask me anything!');

-- Unknown Intent (Fallback)
INSERT INTO responses (intent_id, pattern, response) VALUES
((SELECT id FROM intents WHERE intent_name = 'unknown'), 'unknown query', 'I''m sorry, I didn''t quite understand that. Could you please rephrase your question? You can ask about admissions, courses, fees, placements, or facilities.'),
((SELECT id FROM intents WHERE intent_name = 'unknown'), 'fallback', 'I''m not sure about that. Please try asking in a different way or contact our support team at +91-123-456-7890.');

-- ============================================
-- Create Indexes for Performance
-- ============================================
CREATE INDEX idx_intent_name ON intents(intent_name);
CREATE INDEX idx_is_active ON intents(is_active);
CREATE INDEX idx_username ON admin_users(username);

-- ============================================
-- Grant Permissions (Optional - adjust as needed)
-- ============================================
-- GRANT SELECT, INSERT, UPDATE ON chatbot_db.* TO 'chatbot_user'@'localhost';

-- ============================================
-- Verification Queries
-- ============================================
-- Check data insertion
-- SELECT COUNT(*) as total_intents FROM intents;
-- SELECT COUNT(*) as total_responses FROM responses;
-- SELECT i.intent_name, COUNT(r.id) as pattern_count 
-- FROM intents i LEFT JOIN responses r ON i.id = r.intent_id 
-- GROUP BY i.id;

COMMIT;
