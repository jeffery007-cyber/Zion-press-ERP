import hashlib


class Security:

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password, hashed_password):
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password