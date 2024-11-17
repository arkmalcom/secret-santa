import uuid
from typing import Annotated, Optional

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

DONumberType = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(supported_regions=["DO"], default_region="DO", number_format="RFC3966"),
]


class User(BaseModel):
    """Base class for user to be included in secret santa list."""

    user_public_id: str
    name: str
    phone_number: Optional[DONumberType] = None

    def __init__(self, **data: dict) -> None:
        """Initialize the user with a public id."""
        data["user_public_id"] = data.get("user_public_id", str(uuid.uuid4()))
        super().__init__(**data)


class Pairing(BaseModel):
    """Pairing of users for secret santa."""

    pairing_id: str
    list_id: str
    giving_user: str
    receiving_user: str


class SecretSantaList(BaseModel):
    """Secret Santa that includes a list of users."""

    users: list[User]
