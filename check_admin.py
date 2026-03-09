"""
Check admin credentials in database
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt

# Load environment variables
load_dotenv()

def check_admin():
    """Check admin user in database"""
    
    # Get credentials from .env
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database_name = os.getenv('DB_NAME', 'chatbot_db')
    
    print("=" * 60)
    print("🔍 CHECKING ADMIN CREDENTIALS")
    print("=" * 60)
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        
        if connection.is_connected():
            print("✓ Connected to MySQL database")
            cursor = connection.cursor(dictionary=True)
            
            # Check admin users
            print("\n📋 Current admin users:")
            cursor.execute("SELECT id, username, email, is_active, last_login FROM admin_users")
            admins = cursor.fetchall()
            
            if not admins:
                print("❌ No admin users found!")
                print("\n🔧 Creating default admin user...")
                
                # Create default admin
                default_username = "admin"
                default_password = "admin123"
                password_hash = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
                
                cursor.execute(
                    "INSERT INTO admin_users (username, password_hash, email, is_active) VALUES (%s, %s, %s, %s)",
                    (default_username, password_hash.decode('utf-8'), 'admin@example.com', True)
                )
                connection.commit()
                
                print(f"✅ Created admin user:")
                print(f"   Username: {default_username}")
                print(f"   Password: {default_password}")
            else:
                for admin in admins:
                    print(f"\n  ID: {admin['id']}")
                    print(f"  Username: {admin['username']}")
                    print(f"  Email: {admin['email']}")
                    print(f"  Active: {admin['is_active']}")
                    print(f"  Last Login: {admin['last_login']}")
                
                # Test password verification
                print("\n🔐 Testing password verification...")
                test_username = "admin"
                test_password = "admin123"
                
                cursor.execute("SELECT * FROM admin_users WHERE username = %s", (test_username,))
                admin = cursor.fetchone()
                
                if admin:
                    stored_hash = admin['password_hash']
                    print(f"  Username: {test_username}")
                    print(f"  Trying password: {test_password}")
                    print(f"  Stored hash: {stored_hash[:50]}...")
                    
                    # Verify password
                    try:
                        if bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8')):
                            print("  ✅ Password verification: SUCCESS")
                        else:
                            print("  ❌ Password verification: FAILED")
                            print("\n🔧 Resetting password...")
                            new_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
                            cursor.execute(
                                "UPDATE admin_users SET password_hash = %s WHERE username = %s",
                                (new_hash.decode('utf-8'), test_username)
                            )
                            connection.commit()
                            print("  ✅ Password reset successfully")
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("✅ CHECK COMPLETED")
            print("=" * 60)
            print("\n💡 Default credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n🌐 Login at: http://localhost:5000/login")
            
    except Error as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    check_admin()
