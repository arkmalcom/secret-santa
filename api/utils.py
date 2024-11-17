import random

import boto3
from fastapi import HTTPException

from models import Pairing, User

dynamodb = boto3.resource("dynamodb", region_name="us-east-2")


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


def get_random_pairing(list_id: str, giving_user_id: str) -> dict:
    """Get a random participant from a DynamoDB table."""
    table = dynamodb.Table("secret_santa_participants")

    response = table.scan(
        FilterExpression="list_id = :list_id",
        ExpressionAttributeValues={":list_id": list_id},
    )
    participants = response.get("Items", [])

    if not participants:
        return HTTPException(status_code=404, detail="No participants found")

    random.shuffle(participants)
    random_user = User(**participants[0])
    participant_count = len(participants)
    participants_cycled = 0

    while (
        random_user.user_public_id == giving_user_id
        and not random_user.has_been_assigned
        and participants_cycled < participant_count
    ):
        random.shuffle(participants)
        random_user = User(**participants[0])
        participants_cycled += 1

    if participants_cycled == participant_count:
        return HTTPException(status_code=404, detail="No unassigned participants found")

    return random_user


def get_participant_by_public_id(list_id: str, user_public_id: str) -> dict:
    """Get a participant by public ID from a DynamoDB table."""
    table = dynamodb.Table("secret_santa_participants")

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


def update_assigned_participant(list_id: str, user_public_id: str) -> None:
    """Update the assigned participant in a DynamoDB table."""
    table = dynamodb.Table("secret_santa_participants")

    table.update_item(
        Key={"list_id": list_id, "user_public_id": user_public_id},
        UpdateExpression="SET has_been_assigned = :assigned",
        ExpressionAttributeValues={":assigned": True},
    )


def get_user_pairing(list_id: str, giving_user_id: str) -> dict:
    """Read an item from a DynamoDB table."""
    table = dynamodb.Table("secret_santa_pairings")

    response = table.get_item(Key={"list_id": list_id, "giving_user_id": giving_user_id})
    item = response.get("Item", {})

    if item:
        return Pairing(**item).model_dump()

    return HTTPException(status_code=404, detail="Pairing not found")
