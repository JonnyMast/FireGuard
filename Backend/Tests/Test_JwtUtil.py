import sys
import os
# Add the parent directory (Backend/) to the path so we can import from App
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import jwt
import time
from unittest.mock import Mock
from App.Helpers import JwtUtils
from Tests.Mocks.SupabaseMock import MockDatabase, MockSupabaseService

# Use the same JWT_SECRET as jwt_utils for decoding
JWT_SECRET = JwtUtils.JWT_SECRET


# Test class
class TestJWTFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockDatabase()
        self.supabase_service = MockSupabaseService(self.mock_db)
        self.client_id = "FIRS-t-1a2b"
        self.client_secret = "client-secret-123"
        self.inactive_client_id = "FIRS-t-9z8y"
        self.inactive_client_secret = "client-secret-456"
        self.username = "testuser"
        self.inactive_username = "hello"

    def test_create_and_verify_client_jwt(self):
        token = JwtUtils.CreateClientJwt(self.client_id, self.client_secret)
        self.assertTrue(JwtUtils.VerifyJwt(token, self.supabase_service), "Client JWT should be valid")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], self.client_id)
        self.assertEqual(decoded["client_secret"], self.client_secret)
        self.assertEqual(decoded["type"], "client")

    def test_create_and_verify_user_jwt(self):
        token = JwtUtils.CreateUserJwt(self.username)
        self.assertTrue(JwtUtils.VerifyJwt(token, self.supabase_service), "User JWT should be valid")
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        self.assertEqual(decoded["sub"], self.username)
        self.assertEqual(decoded["type"], "user")
        self.assertNotIn("client_secret", decoded, "User JWT should not have client_secret")

    def test_expired_client_jwt(self):
        original_expiry = JwtUtils.CLIENT_TOKEN_EXPIRY
        JwtUtils.CLIENT_TOKEN_EXPIRY = -1
        token = JwtUtils.CreateClientJwt(self.client_id, self.client_secret)
        JwtUtils.CLIENT_TOKEN_EXPIRY = original_expiry
        self.assertFalse(JwtUtils.VerifyJwt(token, self.supabase_service), "Expired client JWT should be invalid")

    def test_expired_user_jwt(self):
        original_expiry = JwtUtils.USER_TOKEN_EXPIRY
        JwtUtils.USER_TOKEN_EXPIRY = -1
        token = JwtUtils.CreateUserJwt(self.username)
        JwtUtils.USER_TOKEN_EXPIRY = original_expiry
        self.assertFalse(JwtUtils.VerifyJwt(token, self.supabase_service), "Expired user JWT should be invalid")

    def test_invalid_token(self):
        token = JwtUtils.CreateClientJwt(self.client_id, self.client_secret) + "tampered"
        self.assertFalse(JwtUtils.VerifyJwt(token, self.supabase_service), "Tampered token should be invalid")

    def test_inactive_client_jwt(self):
        token = JwtUtils.CreateClientJwt(self.inactive_client_id, self.inactive_client_secret)
        self.assertFalse(JwtUtils.VerifyJwt(token, self.supabase_service), "Inactive client JWT should be invalid")

    def test_inactive_user_jwt(self):
        token = JwtUtils.CreateUserJwt(self.inactive_username)
        self.assertFalse(JwtUtils.VerifyJwt(token, self.supabase_service), "Inactive user JWT should be invalid")

if __name__ == "__main__":
    unittest.main()