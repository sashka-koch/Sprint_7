import requests
import allure
from urls import BASE_URL, GET_ORDERS


class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):

        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(BASE_URL + GET_ORDERS)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)
