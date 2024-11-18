import random

import boto3
from boto3.dynamodb.conditions import Attr, Key
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
    is_not_assigned = False

    response = table.query(
        KeyConditionExpression=Key("list_id").eq(list_id),
        FilterExpression=Attr("has_been_assigned").eq(is_not_assigned),
    )
    participants = response.get("Items", [])

    participants = [participant for participant in participants if participant["user_public_id"] != giving_user_id]

    if not participants:
        raise HTTPException(status_code=404, detail="No participants found")

    random.shuffle(participants)
    return User(**participants[0])


def get_participant_by_public_id(list_id: str, user_public_id: str) -> dict:
    """Get a participant by public ID from a DynamoDB table."""
    table = dynamodb.Table("secret_santa_participants")

    response = table.query(
        KeyConditionExpression=Key("list_id").eq(list_id) & Key("user_public_id").eq(user_public_id),
        Limit=1,
    )
    items = response.get("Items", [])

    if items:
        return User(**items[0])

    raise HTTPException(status_code=404, detail="Participant not found")


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

    raise HTTPException(status_code=404, detail="Pairing not found")


def get_user_from_dynamodb_by_phone(list_id: str, phone_number: str) -> dict:
    """Get a user from a DynamoDB table by phone number."""
    table = dynamodb.Table("secret_santa_participants")

    # Check if the phone number already has hyphens
    if "-" not in phone_number:
        phone_number = f"tel:+1-{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
    else:
        phone_number = f"tel:+1-{phone_number}"

    response = table.query(
        KeyConditionExpression=Key("list_id").eq(list_id),
        FilterExpression=Attr("phone_number").eq(phone_number),
        Limit=1,
    )

    items = response.get("Items", [])

    if items:
        return User(**items[0])

    raise HTTPException(status_code=404, detail="User not found")
