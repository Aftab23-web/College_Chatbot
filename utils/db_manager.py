"""
Database Manager Module
Handles all database operations for the chatbot
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime
import bcrypt

# Load environment variables
load_dotenv()

class DatabaseManager:
    """
    Database connection and operations manager
    """
    
    def __init__(self):
        """Initialize database connection parameters"""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'chatbot_db')
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"✓ Connected to MySQL database: {self.database}")
                return True
        except Error as e:
            print(f"✗ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Execute a database query
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            fetch (bool): Whether to fetch results
            
        Returns:
            list or bool: Query results or success status
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return True
        except Error as e:
            print(f"✗ Query execution error: {e}")
            return [] if fetch else False
        finally:
            if cursor:
                cursor.close()
    
    # ==================== INTENT OPERATIONS ====================
    
    def get_all_intents(self):
        """Get all active intents"""
        query = "SELECT * FROM intents WHERE is_active = TRUE ORDER BY intent_name"
        return self.execute_query(query, fetch=True)
    
    def get_intent_by_name(self, intent_name):
        """Get intent by name"""
        query = "SELECT * FROM intents WHERE intent_name = %s"
        result = self.execute_query(query, (intent_name,), fetch=True)
        return result[0] if result else None
    
    def add_intent(self, intent_name, description=""):
        """Add new intent"""
        query = "INSERT INTO intents (intent_name, description) VALUES (%s, %s)"
        return self.execute_query(query, (intent_name, description))
    
    def update_intent(self, intent_id, intent_name, description):
        """Update existing intent"""
        query = "UPDATE intents SET intent_name = %s, description = %s WHERE id = %s"
        return self.execute_query(query, (intent_name, description, intent_id))
    
    def delete_intent(self, intent_id):
        """Delete intent (sets is_active to FALSE)"""
        query = "UPDATE intents SET is_active = FALSE WHERE id = %s"
        return self.execute_query(query, (intent_id,))
    
    # ==================== RESPONSE OPERATIONS ====================
    
    def get_responses_by_intent(self, intent_id):
        """Get all responses for an intent"""
        query = """
            SELECT r.*, i.intent_name 
            FROM responses r
            JOIN intents i ON r.intent_id = i.id
            WHERE r.intent_id = %s
            ORDER BY r.priority DESC, r.id
        """
        return self.execute_query(query, (intent_id,), fetch=True)
    
    def get_all_responses(self):
        """Get all responses with intent names"""
        query = """
            SELECT r.*, i.intent_name 
            FROM responses r
            JOIN intents i ON r.intent_id = i.id
            ORDER BY i.intent_name, r.priority DESC
        """
        return self.execute_query(query, fetch=True)
    
    def add_response(self, intent_id, pattern, response, priority=0):
        """Add new response"""
        query = """
            INSERT INTO responses (intent_id, pattern, response, priority) 
            VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (intent_id, pattern, response, priority))
    
    def update_response(self, response_id, pattern, response, priority):
        """Update existing response"""
        query = """
            UPDATE responses 
            SET pattern = %s, response = %s, priority = %s 
            WHERE id = %s
        """
        return self.execute_query(query, (pattern, response, priority, response_id))
    
    def delete_response(self, response_id):
        """Delete response"""
        query = "DELETE FROM responses WHERE id = %s"
        return self.execute_query(query, (response_id,))
    
    # ==================== CHAT LOG OPERATIONS ====================
    
    def log_chat(self, user_message, bot_response, predicted_intent, 
                 confidence_score, session_id=None, user_ip=None, user_id=None):
        """Log chat conversation"""
        query = """
            INSERT INTO chat_logs 
            (user_message, bot_response, predicted_intent, confidence_score, session_id, user_ip, user_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        # Convert numpy types to Python native types
        return self.execute_query(query, (
            str(user_message), 
            str(bot_response), 
            str(predicted_intent), 
            float(confidence_score),  # Convert numpy float to Python float
            str(session_id) if session_id else None, 
            str(user_ip) if user_ip else None,
            user_id if user_id else None
        ))
    
    def get_chat_logs(self, limit=100):
        """Get recent chat logs with user information"""
        query = """
            SELECT cl.*, u.username, u.full_name 
            FROM chat_logs cl
            LEFT JOIN users u ON cl.user_id = u.id
            ORDER BY cl.created_at DESC 
            LIMIT %s
        """
        return self.execute_query(query, (limit,), fetch=True)
    
    def get_logs_by_session(self, session_id):
        """Get chat logs for a specific session"""
        query = """
            SELECT * FROM chat_logs 
            WHERE session_id = %s 
            ORDER BY created_at ASC
        """
        return self.execute_query(query, (session_id,), fetch=True)
    
    # ==================== ADMIN OPERATIONS ====================
    
    def verify_admin(self, username, password):
        """Verify admin credentials"""
        query = "SELECT * FROM admin_users WHERE username = %s AND is_active = TRUE"
        result = self.execute_query(query, (username,), fetch=True)
        
        if result:
            admin = result[0]
            try:
                # Verify password using bcrypt
                stored_hash = admin['password_hash']
                if isinstance(stored_hash, str):
                    stored_hash = stored_hash.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    # Update last login
                    self.update_last_login(admin['id'])
                    return admin
            except Exception as e:
                print(f"✗ Password verification error: {e}")
        return None
    
    def update_last_login(self, admin_id):
        """Update admin's last login timestamp"""
        query = "UPDATE admin_users SET last_login = NOW() WHERE id = %s"
        return self.execute_query(query, (admin_id,))
    
    def add_admin(self, username, password, email=None):
        """Add new admin user"""
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = """
            INSERT INTO admin_users (username, password_hash, email) 
            VALUES (%s, %s, %s)
        """
        return self.execute_query(query, (username, password_hash.decode('utf-8'), email))
    
    # ==================== TRAINING DATA EXPORT ====================
    
    def export_training_data(self):
        """
        Export all intents and responses for model training
        
        Returns:
            dict: Training data in intents.json format
        """
        intents = self.get_all_intents()
        training_data = {"intents": []}
        
        for intent in intents:
            responses_data = self.get_responses_by_intent(intent['id'])
            
            if responses_data:
                patterns = []
                responses = []
                
                for response_row in responses_data:
                    # Ensure pattern is not empty/None
                    if response_row['pattern'] and response_row['pattern'].strip():
                        patterns.append(response_row['pattern'].strip())
                    # Ensure response is not empty/None
                    if response_row['response'] and response_row['response'].strip():
                        responses.append(response_row['response'].strip())
                
                # Only add intent if it has both patterns and responses
                if patterns and responses:
                    intent_data = {
                        "tag": intent['intent_name'],
                        "patterns": list(set(patterns)),  # Remove duplicates
                        "responses": list(set(responses))  # Remove duplicates
                    }
                    
                    training_data["intents"].append(intent_data)
                else:
                    print(f"⚠ Skipping intent '{intent['intent_name']}' - missing patterns or responses")
        
        print(f"✓ Exported {len(training_data['intents'])} valid intents for training")
        return training_data


# Example usage and testing
if __name__ == "__main__":
    db = DatabaseManager()
    
    if db.connect():
        # Test: Get all intents
        intents = db.get_all_intents()
        print(f"\nTotal Intents: {len(intents)}")
        for intent in intents[:3]:  # Show first 3
            print(f"  - {intent['intent_name']}: {intent['description']}")
        
        # Test: Get responses for an intent
        if intents:
            intent_id = intents[0]['id']
            responses = db.get_responses_by_intent(intent_id)
            print(f"\nResponses for '{intents[0]['intent_name']}': {len(responses)}")
        
        # Test: Export training data
        training_data = db.export_training_data()
        print(f"\nExported {len(training_data['intents'])} intents for training")
        
        db.disconnect()
