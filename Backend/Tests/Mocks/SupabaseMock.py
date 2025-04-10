class MockDatabase:
    def __init__(self):
        self.api_clients = {
            "FIRS-t-1a2b": {
                "client_id": "FIRS-t-1a2b",
                "client_secret": "client-secret-123",
                "active": True,
            },
            "FIRS-t-9z8y": {
                "client_id": "FIRS-t-9z8y",
                "client_secret": "client-secret-456",
                "active": False,
            },
        }
        self.users = {
            "testuser": {
                "username": "testuser",
                "password_hash": "hashed_password",
                "active": True,
            },
            "hello": {
                "username": "hello",
                "password_hash": "hello_password",
                "active": False,
            },
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


class MockSupabaseService:
    def __init__(self, mock_db=None):
        self.supabase = mock_db or MockDatabase()

    def verify_client(self, client_id, client_secret):
        """Verify client credentials against database"""
        client = self.supabase.api_clients.get(client_id)
        if not client:
            return False
        return client["client_secret"] == client_secret and client["active"]

    def verify_user(self, username):
        """Verify if user exists and is active"""
        user = self.supabase.users.get(username)
        if not user:
            return False
        return user["active"]
