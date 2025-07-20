import unittest
import mysql.connector
<<<<<<< HEAD
import os
import time

class TestSubscribersDB(unittest.TestCase):
    def setUp(self):
        # Get environment variables or use defaults
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'subuser')
        self.password = os.getenv('DB_PASSWORD', 'subpass')
        self.database = os.getenv('DB_NAME', 'subscribers')
        
        # Retry connection with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.conn.cursor()
                break
            except mysql.connector.Error as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        
        # Clean test data before each test
        self.cursor.execute("DELETE FROM subscriber WHERE email LIKE 'testuser%@example.com'")
        self.conn.commit()

    def tearDown(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()

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

=======

class TestSubscribersDB(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='subuser',
            password='subpass',
            database='subscribers'
        )
        self.cursor = self.conn.cursor()
        # Clean test data before each test
        self.cursor.execute("DELETE FROM subscribers WHERE email LIKE 'testuser%@example.com'")
        self.conn.commit()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_create_and_read(self):
        self.cursor.execute("INSERT INTO subscribers (email) VALUES ('testuser1@example.com')")
        self.conn.commit()
        self.cursor.execute("SELECT email FROM subscribers WHERE email = 'testuser1@example.com'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'testuser1@example.com')

    def test_update(self):
        self.cursor.execute("INSERT INTO subscribers (email) VALUES ('testuser2@example.com')")
        self.conn.commit()
        self.cursor.execute("UPDATE subscribers SET status='inactive' WHERE email='testuser2@example.com'")
        self.conn.commit()
        self.cursor.execute("SELECT status FROM subscribers WHERE email='testuser2@example.com'")
        status = self.cursor.fetchone()[0]
        self.assertEqual(status, 'inactive')

    def test_delete(self):
        self.cursor.execute("INSERT INTO subscribers (email) VALUES ('testuser3@example.com')")
        self.conn.commit()
        self.cursor.execute("DELETE FROM subscribers WHERE email='testuser3@example.com'")
        self.conn.commit()
        self.cursor.execute("SELECT * FROM subscribers WHERE email='testuser3@example.com'")
        self.assertIsNone(self.cursor.fetchone())

>>>>>>> f7444b639cdd3cfdaccd957c0f01d62b7dce86e0
if __name__ == '__main__':
    unittest.main()
