import uuid

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from models import SecretSantaList
from utils import generate_secret_santa_pairings

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

    return JSONResponse(
        content={
            "list_id": list_id,
            "message": "Secret Santa list created successfully.",
            "pairings": pairings,
        },
        status_code=201,
    )


@api_router.get("/lists/{list_id}/{user_email}")
def get_user_pairing(list_id: str, user_email: str) -> JSONResponse:
    """Get the secret santa pairing for a user."""
    return JSONResponse(
        content={
            "user_email": user_email,
            "pairing": "Found a pairing",
            "list_id": list_id,
        },
    )


app.include_router(api_router, prefix="/api")
