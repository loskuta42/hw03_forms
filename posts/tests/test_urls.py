from django.test import TestCase, Client


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        cls.guest_client = Client()

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = StaticURLTests.guest_client.get('/')
        self.assertEqual(response.status_code, 200)
