import sys
import os
import requests
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания нового питомца"""
    payload = {"id": 1,
                "name": "Buddy",
                "status": "available"
               }

    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200, "код ответа не совпал с ожидаемым"
    return response.json()