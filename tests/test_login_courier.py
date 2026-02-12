import requests
import allure
from urls import BASE_URL, LOGIN_COURIER


class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_login_success(self, courier):

        with allure.step("Отправка запроса на логин"):
            response = requests.post(
                BASE_URL + LOGIN_COURIER,
                data={
                    "login": courier["login"],
                    "password": courier["password"]
                }
            )

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Ошибка если отсутствует пароль")
    def test_login_without_password(self):

        with allure.step("Авторизация без пароля"):
            response = requests.post(
                BASE_URL + LOGIN_COURIER,
                data={"login": "test"}
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier):

        with allure.step("Авторизация с неверным логином"):
            response = requests.post(
                BASE_URL + LOGIN_COURIER,
                data={
                    "login": "wrong_login",
                    "password": courier["password"]
                }
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_nonexistent_user(self):

        with allure.step("Авторизация несуществующего пользователя"):
            response = requests.post(
                BASE_URL + LOGIN_COURIER,
                data={
                    "login": "nonexistent",
                    "password": "1234"
                }
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 404
