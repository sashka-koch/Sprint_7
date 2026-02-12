import pytest
import requests
import allure
from helpers.courier_helper import generate_random_string, delete_courier
from urls import BASE_URL, CREATE_COURIER, LOGIN_COURIER


@pytest.fixture
def courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    with allure.step("Создание курьера (fixture setup)"):
        response = requests.post(BASE_URL + CREATE_COURIER, data=payload)
        assert response.status_code == 201

    yield {
        "login": login,
        "password": password,
        "first_name": first_name
    }

    with allure.step("Удаление курьера (fixture teardown)"):
        login_response = requests.post(
            BASE_URL + LOGIN_COURIER,
            data={"login": login, "password": password}
        )
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_courier(courier_id)
