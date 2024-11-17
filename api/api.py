import uuid

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from models import Pairing, SecretSantaList
from utils import (
    batch_write_to_dynamodb,
    get_pairing_from_dynamodb,
    get_participant_by_public_id,
    get_random_participant,
    write_to_dynamodb,
)

app = FastAPI()
api_router = APIRouter()


@api_router.post("/lists/create")
async def create_secret_santa_list(secret_santa_list: SecretSantaList) -> JSONResponse:
    """Create a new secret santa list."""
    user_list = secret_santa_list.users
    if len(user_list) < 2:
        raise HTTPException(status_code=400, detail="At least two users are required")

    list_id = str(uuid.uuid4())

    participants = [{"list_id": list_id, **user.model_dump()} for user in user_list]

    batch_write_to_dynamodb("secret_santa_participants", participants)

    return JSONResponse(
        content={
            "list_id": list_id,
            "message": "Secret Santa list created successfully.",
        },
        status_code=201,
    )


@api_router.get("/pairings/create/{list_id}/{user_public_id}")
def create_secret_santa_pairing(list_id: str, user_public_id: str) -> JSONResponse:
    """Create a secret santa pairing for a user."""
    random_participant = get_random_participant("secret_santa_participants", list_id)
    giving_user = get_participant_by_public_id("secret_santa_participants", list_id, user_public_id)

    while random_participant.user_public_id == user_public_id:
        random_participant = get_random_participant("secret_santa_participants", list_id)

    pairing_id = str(uuid.uuid4())
    pairing = Pairing(
        pairing_id=pairing_id,
        list_id=list_id,
        giving_user=giving_user.name,
        receiving_user=random_participant.name,
    )

    write_to_dynamodb("secret_santa_pairing", pairing.model_dump())

    return JSONResponse(
        content={"message": "Successfully created secret santa pairing."},
        status_code=201,
    )


@api_router.get("/pairings/{pairing_id}/{list_id}")
def get_user_pairing(list_id: str, pairing_id: str) -> JSONResponse:
    """Get the secret santa pairing for a user."""
    pairing = get_pairing_from_dynamodb("secret_santa_pairing", pairing_id, list_id)

    return JSONResponse(
        content={
            **pairing,
            "list_id": list_id,
        },
    )


app.include_router(api_router, prefix="/api")

handler = Mangum(app)
