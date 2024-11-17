import random
import uuid

import boto3
from fastapi import HTTPException

from models import Pairing, User

dynamodb = boto3.resource("dynamodb", region_name="us-east-2")


def generate_secret_santa_pairings(users: list[User]) -> dict[str, str]:
    """Generate secret santa pairings for a list of users."""
    user_names = [user.name for user in users]
    random.shuffle(user_names)

    pairings = []

    for i, user in enumerate(users):
        receiving_user = user_names[i]
        while receiving_user == user.name:
            random.shuffle(user_names)
            receiving_user = user_names[i]

        pairing_id = str(uuid.uuid4())
        pairing = Pairing(
            pairing_id=pairing_id,
            giving_user=user.name,
            receiving_user=receiving_user,
        )
        pairings.append(pairing.model_dump())

    return pairings


def write_to_dynamodb(table_name: str, item: dict) -> None:
    """Write an item to a DynamoDB table."""
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)


def batch_write_to_dynamodb(table_name: str, items: list[dict]) -> None:
    """Write an item to a DynamoDB table."""
    table = dynamodb.Table(table_name)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


def get_random_participant(table_name: str, list_id: str) -> dict:
    """Get a random participant from a DynamoDB table."""
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression="list_id = :list_id",
        ExpressionAttributeValues={":list_id": list_id},
    )
    items = response.get("Items", [])

    if items:
        random.shuffle(items)
        return User(**items[0])

    return HTTPException(status_code=404, detail="No participants found")


def get_participant_by_public_id(table_name: str, list_id: str, user_public_id: str) -> dict:
    """Get a participant by public ID from a DynamoDB table."""
    table = dynamodb.Table(table_name)

    response = table.scan(
        FilterExpression="list_id = :list_id AND user_public_id = :user_public_id",
        ExpressionAttributeValues={
            ":list_id": list_id,
            ":user_public_id": user_public_id,
        },
        Limit=1,
    )
    items = response.get("Items", [])

    if items:
        return User(**items[0])

    return HTTPException(status_code=404, detail="Participant not found")


def get_pairing_from_dynamodb(table_name: str, pairing_id: str, list_id: str) -> dict:
    """Read an item from a DynamoDB table."""
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={"pairing_id": pairing_id, "list_id": list_id})
    item = response.get("Item", {})

    if item:
        return Pairing(**item).model_dump()

    return HTTPException(status_code=404, detail="Pairing not found")
