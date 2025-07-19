import unittest
import mysql.connector

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

if __name__ == '__main__':
    unittest.main()
