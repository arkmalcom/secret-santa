from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(BaseModel):
    """Base class for user to be included in secret santa list."""

    name: str
    phone_number: PhoneNumber


class Pairing(BaseModel):
    """Pairing of users for secret santa."""

    pairing_id: str
    giving_user: str
    receiving_user: str


class SecretSantaList(BaseModel):
    """Secret Santa that includes a list of users."""

    users: list[User]
