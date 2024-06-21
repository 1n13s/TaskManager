from fastapi import APIRouter
from starlette import status
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/",status_code=status.HTTP_200_OK)
def test_connection():
    """Root"""
    return JSONResponse(content={"message":"Connected successfully"}, status_code=status.HTTP_200_OK)