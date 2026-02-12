import requests
import allure
from helpers.courier_helper import (
    BASE_URL,
    register_new_courier_and_return_login_password,
    delete_courier
)


class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login_successfully(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 200

        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

        delete_courier(response.json()["id"])

    @allure.title("Для авторизации нужно передать все обязательные поля")
    def test_login_requires_all_required_fields(self):
        payload = {
            "login": "some_login"
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при неправильном логине")
    def test_login_with_wrong_login_returns_error(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data

        payload = {
            "login": "wrong_login",
            "password": password
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert "message" in response.json()

        login_response = requests.post(BASE_URL + "courier/login", data={
            "login": login,
            "password": password
        })
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)

    @allure.title("Ошибка при неправильном пароле")
    def test_login_with_wrong_password_returns_error(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data

        payload = {
            "login": login,
            "password": "wrong_password"
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert "message" in response.json()

        login_response = requests.post(BASE_URL + "courier/login", data={
            "login": login,
            "password": password
        })
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)

    @allure.title("Ошибка если отсутствует логин")
    def test_login_without_login_returns_error(self):
        payload = {
            "password": "1234"
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка если отсутствует пароль")
    def test_login_without_password_returns_error(self):
        payload = {
            "login": "some_login"
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_login_nonexistent_user_returns_error(self):
        payload = {
            "login": "nonexistent_user",
            "password": "1234"
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Успешный запрос возвращает id")
    def test_successful_login_returns_id(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(BASE_URL + "courier/login", data=payload)

        assert response.status_code == 200
        assert "id" in response.json()
        assert type(response.json()["id"]) is int

        delete_courier(response.json()["id"])
