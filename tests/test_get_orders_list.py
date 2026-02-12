import requests
import allure
from helpers.courier_helper import BASE_URL


class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        response = requests.get(BASE_URL + "orders")

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
