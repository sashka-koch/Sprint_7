import requests
import allure
from helpers.courier_helper import generate_random_string
from urls import BASE_URL, CREATE_COURIER


class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(BASE_URL + CREATE_COURIER, data=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201

        with allure.step("Проверка тела ответа"):
            assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier):
        payload = {
            "login": courier["login"],
            "password": courier["password"],
            "firstName": courier["first_name"]
        }

        with allure.step("Повторная попытка создания курьера"):
            response = requests.post(BASE_URL + CREATE_COURIER, data=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400

        with allure.step("Проверка тела ответа"):
            assert response.json()["message"] == "Этот логин уже используется"

    @allure.title("Ошибка если отсутствует логин")
    def test_create_courier_without_login(self):
        payload = {
            "password": "1234",
            "firstName": "test"
        }

        with allure.step("Создание курьера без логина"):
            response = requests.post(BASE_URL + CREATE_COURIER, data=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400

        with allure.step("Проверка текста ошибки"):
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка если отсутствует пароль")
    def test_create_courier_without_password(self):
        payload = {
            "login": "testlogin",
            "firstName": "test"
        }

        with allure.step("Создание курьера без пароля"):
            response = requests.post(BASE_URL + CREATE_COURIER, data=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400

        with allure.step("Проверка текста ошибки"):
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
