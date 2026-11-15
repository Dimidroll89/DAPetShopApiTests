import allure
import requests

BASE_URL = "https://petstore.swagger.rv-school.ru/api/v3"

@allure.feature("pet")
class TestPet:
    @allure.title("попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статсуса ответа"):
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

        with allure.step("Проверка статсуса ответа"):
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
