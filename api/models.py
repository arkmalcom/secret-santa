from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    """Base class for user to be included in secret santa list."""

    name: str
    email: EmailStr


class SecretSantaList(BaseModel):
    """Secret Santa that includes a list of users."""

    users: list[User]

    @field_validator("users")
    @classmethod
    def validate_users(cls, users: list[User]) -> list[User]:
        """Ensure users are unique."""
        unique_user_count = len({user.email for user in users})

        if unique_user_count != len(users):
            raise HTTPException(status_code=400, detail="User emails must be unique.")

        return users
