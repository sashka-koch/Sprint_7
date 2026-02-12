import requests
import pytest
import allure
from helpers.courier_helper import BASE_URL
from data.order_data import order_body


class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None
        ]
    )
    def test_create_order_with_different_colors(self, color):
        payload = order_body.copy()


        if color is not None:
            payload["color"] = color

        response = requests.post(BASE_URL + "orders", json=payload)


        assert response.status_code == 201


        response_body = response.json()
        assert "track" in response_body
        assert isinstance(response_body["track"], int)
