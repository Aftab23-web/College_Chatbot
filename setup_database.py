"""
Database Setup Script
Creates database and tables from schema.sql
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Setup the database and create tables"""
    
    # Get credentials from .env
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database_name = os.getenv('DB_NAME', 'chatbot_db')
    
    print("=" * 60)
    print("🗄️  MYSQL DATABASE SETUP")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"User: {user}")
    print(f"Database: {database_name}")
    print(f"Password: {'*' * len(password) if password else '(empty)'}")
    print()
    
    try:
        # Connect without database first
        print("📡 Connecting to MySQL server...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✓ Connected to MySQL server")
            cursor = connection.cursor()
            
            # Create database
            print(f"\n📊 Creating database '{database_name}'...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✓ Database '{database_name}' created/verified")
            
            # Use the database
            cursor.execute(f"USE {database_name}")
            
            # Read and execute schema.sql
            print("\n📜 Reading schema.sql...")
            schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
            
            if not os.path.exists(schema_path):
                print(f"✗ Schema file not found: {schema_path}")
                return False
            
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            print("✓ Schema file loaded")
            
            # Split by semicolons and execute each statement
            print("\n🔨 Creating tables...")
            statements = schema_sql.split(';')
            
            for statement in statements:
                statement = statement.strip()
                if statement:  # Skip empty statements
                    try:
                        cursor.execute(statement)
                        print("✓", end=" ", flush=True)
                    except Error as e:
                        # Ignore table already exists errors
                        if "already exists" not in str(e):
                            print(f"\n⚠️  Warning: {e}")
            
            connection.commit()
            print("\n✓ All tables created successfully")
            
            # Verify tables
            print("\n📋 Verifying tables...")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"✓ Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"  - {table[0]}: {count} rows")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("✅ DATABASE SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\n🚀 You can now restart the application:")
            print("   python app.py")
            print("\n")
            return True
            
    except Error as e:
        print(f"\n✗ Error: {e}")
        print("\n❌ DATABASE SETUP FAILED")
        print("\nCommon solutions:")
        print("  1. Make sure MySQL is installed and running")
        print("  2. Check your .env file has correct credentials")
        print("  3. Verify MySQL password is correct")
        print("  4. Try resetting MySQL root password")
        return False

if __name__ == "__main__":
    setup_database()
