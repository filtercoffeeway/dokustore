import secrets

class auth:
    @staticmethod
    def generate_token(length=50):
        """Generate a random authentication token."""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        return token
