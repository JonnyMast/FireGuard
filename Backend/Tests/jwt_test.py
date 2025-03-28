import sys
import os
# Add the parent directory (Backend/) to the path so we can import from App
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import jwt
import time
from unittest.mock import Mock
from App.Helpers import jwt_utils

# Use the same JWT_SECRET as jwt_utils for decoding
JWT_SECRET = jwt_utils.JWT_SECRET

# Mock database class to simulate Supabase
class MockDatabase:
    def __init__(self):
        self.api_clients = {
            "FIRS-t-1a2b": {"client_id": "FIRS-t-1a2b", "client_secret": "client-secret-123", "active": True},
            "FIRS-t-9z8y": {"client_id": "FIRS-t-9z8y", "client_secret": "client-secret-456", "active": False}
        }
        self.users = {
            "testuser": {"username": "testuser", "password_hash": "hashed_password", "active": True},
            "hello": {"username": "hello", "password_hash": "hello_password", "active": False}
        }

    def table(self, table_name):
        return MockQueryBuilder(self, table_name)

class MockQueryBuilder:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.conditions = {}

    def select(self, *args):
        return self

    def eq(self, column, value):
        self.conditions[column] = value
        return self

    def execute(self):
        if self.table_name == "api_clients":
            data = self.db.api_clients.get(self.conditions.get("client_id"))
        elif self.table_name == "users":
            data = self.db.users.get(self.conditions.get("username"))
        return MockResult([data] if data else [])

class MockResult:
    def __init__(self, data):
        self.data = data

# Test class
class TestJWTFunctions(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase()
        self.client_id = "FIRS-t-1a2b"
        self.client_secret = "client-secret-123"
        self.inactive_client_id = "FIRS-t-9z8y"
        self.inactive_client_secret = "client-secret-456"
        self.username = "testuser"
        self.inactive_username = "hello"

    def test_create_and_verify_client_jwt(self):
        token = jwt_utils.create_client_jwt(self.client_id, self.client_secret)
        self.assertTrue(jwt_utils.verify_jwt(token, self.db), "Client JWT should be valid")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], self.client_id)
        self.assertEqual(decoded["client_secret"], self.client_secret)
        self.assertEqual(decoded["type"], "client")

    def test_create_and_verify_user_jwt(self):
        token = jwt_utils.create_user_jwt(self.username)
        self.assertTrue(jwt_utils.verify_jwt(token, self.db), "User JWT should be valid")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], self.username)
        self.assertEqual(decoded["type"], "user")
        self.assertNotIn("client_secret", decoded, "User JWT should not have client_secret")

    def test_expired_client_jwt(self):
        original_expiry = jwt_utils.CLIENT_TOKEN_EXPIRY
        jwt_utils.CLIENT_TOKEN_EXPIRY = -1
        token = jwt_utils.create_client_jwt(self.client_id, self.client_secret)
        jwt_utils.CLIENT_TOKEN_EXPIRY = original_expiry
        self.assertFalse(jwt_utils.verify_jwt(token, self.db), "Expired client JWT should be invalid")

    def test_expired_user_jwt(self):
        original_expiry = jwt_utils.USER_TOKEN_EXPIRY
        jwt_utils.USER_TOKEN_EXPIRY = -1
        token = jwt_utils.create_user_jwt(self.username)
        jwt_utils.USER_TOKEN_EXPIRY = original_expiry
        self.assertFalse(jwt_utils.verify_jwt(token, self.db), "Expired user JWT should be invalid")

    def test_invalid_token(self):
        token = jwt_utils.create_client_jwt(self.client_id, self.client_secret) + "tampered"
        self.assertFalse(jwt_utils.verify_jwt(token, self.db), "Tampered token should be invalid")

    def test_inactive_client_jwt(self):
        token = jwt_utils.create_client_jwt(self.inactive_client_id, self.inactive_client_secret)
        self.assertFalse(jwt_utils.verify_jwt(token, self.db), "Inactive client JWT should be invalid")

    def test_inactive_user_jwt(self):
        token = jwt_utils.create_user_jwt(self.inactive_username)
        self.assertFalse(jwt_utils.verify_jwt(token, self.db), "Inactive user JWT should be invalid")

if __name__ == "__main__":
    unittest.main()