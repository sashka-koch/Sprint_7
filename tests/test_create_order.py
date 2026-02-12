import requests
import pytest
import allure
from urls import BASE_URL, CREATE_ORDER
from data.order_data import order_body


class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "payload",
        [
            {**order_body, "color": ["BLACK"]},
            {**order_body, "color": ["GREY"]},
            {**order_body, "color": ["BLACK", "GREY"]},
            order_body  # без цвета вообще
        ]
    )
    def test_create_order_with_different_colors(self, payload):

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(BASE_URL + CREATE_ORDER, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 201

        with allure.step("Проверка наличия track в ответе"):
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)
