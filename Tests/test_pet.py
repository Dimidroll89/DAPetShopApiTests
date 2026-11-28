import allure
import requests
import jsonschema

from schemas.pet_schema import PET_SCHEMA


BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

@allure.feature("pet")
class TestPet:
    @allure.title("попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержания ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                   "name": "Non-existent Pet",
                   "status": "available"
                   }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержания ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("попытка получить информацию о несуществующем питомце")
    def test_getinfo_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статсуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержания ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title ("добавление нового питомца")
    def test_add_nonexistent_pet(self):
        with allure.step("подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"}

        with allure.step("Отправка на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статсуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответа"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("добавление нового питомца c полными данными")
    def test_add_nonexistent_full_data_pet(self):
        with allure.step("подготовка данных для создания питомца c полными данными"):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {"id": 1, "name": "Dogs"},
                       "photoUrls": ["string"],
                       "tags": [{"id": 0, "name": "string"}],
                       "status": "available"
                       }

        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца с полными данными в ответа"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомца не совпадает с ожидаемым"

    @allure.title("получение иформации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("отправка запроса на получение информиции о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("проверка статуса ответа и данных о питомце"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "ID питомца не совпало с ожидаемым"

    @allure.title("Обновление информации о питомце")
    def test_update_pet(self, create_pet):
        with allure.step("получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("подготовка данных для обновления информации о питомце"):
            payload = {"id": pet_id,
                       "name": "Buddy Updated",
                       "status": "sold"}

        with allure.step("отправка запроса на обновление информиции о питомце по ID"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("проверка статуса ответа и данных о питомце"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"
            assert response.json()["name"] == payload["name"], "имя питомца не совпало с ожидаемым"
            assert response.json()["id"] == payload["id"], "ID питомца не совпало с ожидаемым"
            assert response.json()["status"] == payload["status"], "статус питомца не совпало с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("отправка запроса на удаление питомца по ID"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"

        with allure.step("отправка запроса на получение информиции о удаленном питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"



