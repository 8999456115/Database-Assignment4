#!/usr/bin/env python3
"""
Simple MySQL connection test script
"""
import mysql.connector
import os
import sys

def test_connection():
    try:
        # Get environment variables or use defaults
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USER', 'subuser')
        password = os.getenv('DB_PASSWORD', 'subpass')
        database = os.getenv('DB_NAME', 'subscribers')
        
        print(f"Attempting to connect to MySQL at {host}...")
        print(f"User: {user}")
        print(f"Database: {database}")
        
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ MySQL connection successful!")
            
            # Check if subscriber table exists
            cursor.execute("SHOW TABLES LIKE 'subscriber'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                print("✅ Subscriber table exists!")
                
                # Check table structure
                cursor.execute("DESCRIBE subscriber")
                columns = cursor.fetchall()
                print("📋 Table structure:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
            else:
                print("❌ Subscriber table does not exist")
                
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Docker is running")
        print("2. Check if MySQL container is started")
        print("3. Verify environment variables in .env file")
        return False
    
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 