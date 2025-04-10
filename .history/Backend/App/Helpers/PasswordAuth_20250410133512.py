import bcrypt

class PasswordAuth:

    def CryptPass(self, password:str) -> str:
        """This function is for creating a hash from a password for storing in database"""
        try:
            return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        
    def CheckPass(self, input_pass:str, database_pass:str) -> bool:
        """This function checks raw input 'pass123' up with the hash stored in the database '98jv8aqou4rf7'"""
        try: 
            return bcrypt.checkpw(input_pass.encode("utf-8"), database_pass.encode("utf-8"))

        
password_auth = PasswordAuth()