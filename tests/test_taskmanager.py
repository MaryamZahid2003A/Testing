import unittest
import time
import random
import string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class TaskManagerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')  # Disable for debugging
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        chrome_service = Service("/usr/bin/chromedriver")
        cls.driver = webdriver.Chrome(service=chrome_service, options=options)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.implicitly_wait(3)

        cls.base_url = "http://localhost"
        cls.username = ''.join(random.choices(string.ascii_lowercase, k=6))
        cls.password = "test123"

    def test_01_signup(self):
        self.driver.get(f"{self.base_url}/signup.php")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_02_add_task(self):
        self.driver.get(f"{self.base_url}/add.php")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "title"))).send_keys("Test Task")
        self.driver.find_element(By.NAME, "description").send_keys("This is a test description.")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_03_task_appears_on_dashboard(self):
        self.driver.get(f"{self.base_url}/index.php")
        rows = self.driver.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any("Test Task" in row.text for row in rows))

    def test_04_edit_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        try:
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))).click()
        except NoSuchElementException:
            self.fail("Edit button not found for any task")

        title_input = self.wait.until(EC.presence_of_element_located((By.NAME, "title")))
        title_input.clear()
        title_input.send_keys("Updated Task")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_05_verify_task_updated(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.assertIn("Updated Task", self.driver.page_source)

    def test_06_delete_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        try:
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Delete"))).click()
            alert = self.driver.switch_to.alert
            alert.accept()
            time.sleep(1)
        except NoSuchElementException:
            self.fail("Delete link not found.")

        self.assertNotIn("Updated Task", self.driver.page_source)

    def test_07_logout(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
        self.assertIn("login.php", self.driver.current_url)

    def test_08_login_with_correct_credentials(self):
        self.driver.get(f"{self.base_url}/login.php")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_09_login_with_wrong_password(self):
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/login.php")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("Invalid password", self.driver.page_source)

    def test_10_login_with_nonexistent_user(self):
        self.driver.get(f"{self.base_url}/login.php")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys("notarealuser123")
        self.driver.find_element(By.NAME, "password").send_keys("somepassword")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("User not found", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
