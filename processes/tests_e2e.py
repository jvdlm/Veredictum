from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class VeredictumE2ETest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def tearDown(self):
        self.browser.quit()

    def test_login_e_acessa_processos(self):
        self.browser.get(self.live_server_url + "/login/")
        wait = WebDriverWait(self.browser, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "username")))
        self.assertIsNotNone(self.browser.get_cookie("csrftoken"))

        self.browser.find_element(By.NAME, "username").send_keys("testuser")
        self.browser.find_element(By.NAME, "password").send_keys("testpass123")
        self.browser.find_element(By.NAME, "password").submit()

        wait.until(EC.url_to_be(f"{self.live_server_url}/"))
        self.browser.get(self.live_server_url + "/processes/")
        self.assertIn("/processes", self.browser.current_url)

    def test_pagina_processos_tem_filtros(self):
        self.client.login(username="testuser", password="testpass123")
        cookie = self.client.cookies["sessionid"]
        self.browser.get(self.live_server_url + "/")
        self.browser.add_cookie(
            {
                "name": "sessionid",
                "value": cookie.value,
                "path": "/",
            }
        )
        self.browser.get(self.live_server_url + "/processes/")

        self.assertTrue(self.browser.find_element(By.NAME, "status"))
        self.assertTrue(self.browser.find_element(By.NAME, "busca"))
