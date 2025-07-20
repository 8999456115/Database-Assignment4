import unittest
import mysql.connector
import os
import time

class TestSubscribersDB(unittest.TestCase):
    def setUp(self):
        # Get environment variables or use defaults for container connection
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', 'root123')  # Use the password from MySQL container
        self.database = os.getenv('DB_NAME', 'subscribers')
        
        # Retry connection with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=3306,
                    auth_plugin='mysql_native_password'
                )
                self.cursor = self.conn.cursor()
                print(f"✅ Successfully connected to database: {self.database}")
                break
            except mysql.connector.Error as e:
                print(f"❌ Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        
        # Clean test data before each test
        try:
            self.cursor.execute("DELETE FROM subscriber WHERE email LIKE 'testuser%@example.com'")
            self.conn.commit()
            print("✅ Test data cleaned")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean test data: {e}")

    def tearDown(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        print("✅ Database connection closed")

    def test_create_subscriber(self):
        """Test creating a new subscriber"""
        email = 'testuser1@example.com'
        self.cursor.execute("INSERT INTO subscriber (email) VALUES (%s)", (email,))
        self.conn.commit()
        
        # Verify the subscriber was created
        self.cursor.execute("SELECT email FROM subscriber WHERE email = %s", (email,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], email)
        print(f"✅ Created subscriber: {email}")

    def test_read_subscriber(self):
        """Test reading subscriber data"""
        email = 'testuser2@example.com'
        name = 'Test User 2'
        
        # Insert test data
        self.cursor.execute("INSERT INTO subscriber (email, name) VALUES (%s, %s)", (email, name))
        self.conn.commit()
        
        # Read the data
        self.cursor.execute("SELECT email, name FROM subscriber WHERE email = %s", (email,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], email)
        self.assertEqual(result[1], name)
        print(f"✅ Read subscriber: {email}")

    def test_update_subscriber(self):
        """Test updating subscriber information"""
        email = 'testuser3@example.com'
        original_name = 'Original Name'
        updated_name = 'Updated Name'
        
        # Insert test data
        self.cursor.execute("INSERT INTO subscriber (email, name) VALUES (%s, %s)", (email, original_name))
        self.conn.commit()
        
        # Update the name
        self.cursor.execute("UPDATE subscriber SET name = %s WHERE email = %s", (updated_name, email))
        self.conn.commit()
        
        # Verify the update
        self.cursor.execute("SELECT name FROM subscriber WHERE email = %s", (email,))
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], updated_name)
        print(f"✅ Updated subscriber: {email}")

    def test_delete_subscriber(self):
        """Test deleting a subscriber"""
        email = 'testuser4@example.com'
        
        # Insert test data
        self.cursor.execute("INSERT INTO subscriber (email) VALUES (%s)", (email,))
        self.conn.commit()
        
        # Verify it exists
        self.cursor.execute("SELECT * FROM subscriber WHERE email = %s", (email,))
        self.assertIsNotNone(self.cursor.fetchone())
        
        # Delete the subscriber
        self.cursor.execute("DELETE FROM subscriber WHERE email = %s", (email,))
        self.conn.commit()
        
        # Verify it was deleted
        self.cursor.execute("SELECT * FROM subscriber WHERE email = %s", (email,))
        self.assertIsNone(self.cursor.fetchone())
        print(f"✅ Deleted subscriber: {email}")

    def test_unique_email_constraint(self):
        """Test that email addresses must be unique"""
        email = 'testuser5@example.com'
        
        # Insert first subscriber
        self.cursor.execute("INSERT INTO subscriber (email) VALUES (%s)", (email,))
        self.conn.commit()
        
        # Try to insert duplicate email
        with self.assertRaises(mysql.connector.IntegrityError):
            self.cursor.execute("INSERT INTO subscriber (email) VALUES (%s)", (email,))
            self.conn.commit()
        print(f"✅ Verified unique constraint for: {email}")

    def test_list_all_subscribers(self):
        """Test listing all subscribers"""
        # Insert multiple test subscribers
        test_emails = [
            'testuser6@example.com',
            'testuser7@example.com',
            'testuser8@example.com'
        ]
        
        for email in test_emails:
            self.cursor.execute("INSERT INTO subscriber (email) VALUES (%s)", (email,))
        self.conn.commit()
        
        # Get all subscribers
        self.cursor.execute("SELECT email FROM subscriber WHERE email LIKE 'testuser%@example.com' ORDER BY email")
        results = self.cursor.fetchall()
        
        # Verify we got all test subscribers
        self.assertEqual(len(results), len(test_emails))
        result_emails = [row[0] for row in results]
        for email in test_emails:
            self.assertIn(email, result_emails)
        print(f"✅ Listed {len(test_emails)} subscribers")

if __name__ == '__main__':
    unittest.main()
