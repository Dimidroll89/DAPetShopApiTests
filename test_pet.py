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

