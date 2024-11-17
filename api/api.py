import uuid

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from models import SecretSantaList
from utils import (
    generate_secret_santa_pairings,
    get_pairing_from_dynamodb,
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
    pairings = generate_secret_santa_pairings(user_list)

    items_to_write = [{"list_id": list_id, **pairing} for pairing in pairings]
    write_to_dynamodb("secret_santa_pairing", items_to_write)

    return JSONResponse(
        content={
            "list_id": list_id,
            "message": "Secret Santa list created successfully.",
            "pairings": pairings,
        },
        status_code=201,
    )


@api_router.get("/lists/{pairing_id}/{list_id}")
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
