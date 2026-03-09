"""
Update database schema to add user authentication support
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def update_database():
    """Add users table and update chat_logs"""
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'chatbot_db')
        )
        
        cursor = connection.cursor()
        
        print("=" * 60)
        print("Updating database schema...")
        print("=" * 60)
        
        # Create users table
        print("\n1. Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX idx_username (username)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        print("✓ Users table created")
        
        # Check if user_id column exists in chat_logs
        print("\n2. Checking chat_logs table...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'chat_logs' 
            AND COLUMN_NAME = 'user_id'
            AND TABLE_SCHEMA = DATABASE()
        """)
        
        column_exists = cursor.fetchone()[0] > 0
        
        if not column_exists:
            print("   Adding user_id column to chat_logs...")
            cursor.execute("ALTER TABLE chat_logs ADD COLUMN user_id INT NULL AFTER id")
            print("✓ user_id column added")
            
            # Add foreign key
            print("   Adding foreign key constraint...")
            try:
                cursor.execute("""
                    ALTER TABLE chat_logs 
                    ADD CONSTRAINT fk_chat_logs_user 
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                """)
                print("✓ Foreign key constraint added")
            except mysql.connector.Error as e:
                if 'Duplicate' in str(e):
                    print("   Foreign key already exists")
                else:
                    print(f"   Warning: Could not add foreign key: {e}")
            
            # Add index
            print("   Adding index for user_id...")
            try:
                cursor.execute("CREATE INDEX idx_user_id ON chat_logs(user_id)")
                print("✓ Index added")
            except mysql.connector.Error as e:
                if 'Duplicate' in str(e):
                    print("   Index already exists")
                else:
                    print(f"   Warning: Could not add index: {e}")
        else:
            print("✓ user_id column already exists")
        
        connection.commit()
        
        print("\n" + "=" * 60)
        print("✓ Database schema updated successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Register new users through the chat interface")
        print("2. View user information in admin panel chat logs")
        print("3. Track which user asked which questions")
        
    except mysql.connector.Error as e:
        print(f"\n✗ Database error: {e}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == '__main__':
    update_database()
