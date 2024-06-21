from fastapi.testclient import TestClient
#from ApiTaskManager.app import app
from fastapi import status
from ..ApiTaskManager.core.user_manager import UserManager

def test_user():
    user = UserManager()
    assert type(user.get_all_users()) == dict


"""client = TestClient(app)

def test_return_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message":"Connected successfully"}"""