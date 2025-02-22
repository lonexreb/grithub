# repositories/user_repository.py
from typing import Dict, Optional
from models.user_model import User
import uuid

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}

    def create_user(self, email: str, hashed_password: str) -> User:
        user_id = str(uuid.uuid4())
        user = User(id=user_id, email=email, hashed_password=hashed_password)
        self._users[user_id] = user
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return next((user for user in self._users.values() if user.email == email), None)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

# Singleton instance for reuse in authentication services
user_repository_instance = UserRepository()
