from fastapi import APIRouter

router = APIRouter()

@router.get("/deployments/test")
def test_route():
    return {"message": "Deployments route is working"}