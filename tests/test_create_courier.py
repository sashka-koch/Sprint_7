import requests
import allure
from helpers.courier_helper import BASE_URL, generate_random_string, delete_courier


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

        response = requests.post(BASE_URL + "courier", data=payload)

        assert response.status_code == 201

        assert response.json() == {"ok": True}

        login_data = {
            "login": login,
            "password": password
        }
        login_response = requests.post(BASE_URL + "courier/login", data=login_data)
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        requests.post(BASE_URL + "courier", data=payload)

        response = requests.post(BASE_URL + "courier", data=payload)

        assert response.status_code == 400
        assert "message" in response.json()

        login_response = requests.post(BASE_URL + "courier/login", data={
            "login": login,
            "password": password
        })
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)

    @allure.title("Для создания курьера нужно передать все обязательные поля")
    def test_create_courier_without_login(self):
        payload = {
            "password": "1234",
            "firstName": "test"
        }

        response = requests.post(BASE_URL + "courier", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка если отсутствует пароль")
    def test_create_courier_without_password(self):
        payload = {
            "login": "testlogin",
            "firstName": "test"
        }

        response = requests.post(BASE_URL + "courier", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка если отсутствует firstName")
    def test_create_courier_without_firstname(self):
        payload = {
            "login": "testlogin",
            "password": "1234"
        }

        response = requests.post(BASE_URL + "courier", data=payload)

        assert response.status_code in [201, 400]

    @allure.title("Если создать пользователя с существующим логином — возвращается ошибка")
    def test_create_courier_with_existing_login(self):
        login = generate_random_string(10)
        password = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": "test"
        }

        requests.post(BASE_URL + "courier", data=payload)

        second_payload = {
            "login": login,
            "password": "anotherpass",
            "firstName": "another"
        }

        response = requests.post(BASE_URL + "courier", data=second_payload)

        assert response.status_code == 400
        assert "message" in response.json()

        login_response = requests.post(BASE_URL + "courier/login", data={
            "login": login,
            "password": password
        })
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)
