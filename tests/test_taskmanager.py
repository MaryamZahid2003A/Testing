import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import string

class TaskManagerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.base_url = "http://107.22.131.95"
        cls.username = ''.join(random.choices(string.ascii_lowercase, k=6))
        cls.password = "test123"

    def test_01_signup(self):
        self.driver.get(f"{self.base_url}/signup.php")
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys(type(self).password)
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_02_add_task(self):
        self.driver.get(f"{self.base_url}/add.php")
        self.driver.find_element(By.NAME, "title").send_keys("Test Task")
        self.driver.find_element(By.NAME, "description").send_keys("This is a test description.")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_03_task_appears_on_dashboard(self):
        self.driver.get(f"{self.base_url}/index.php")
        tasks = self.driver.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any("Test Task" in t.text for t in tasks))

    def test_04_edit_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys("Updated Task")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_05_verify_task_updated(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.assertTrue("Updated Task" in self.driver.page_source)

    def test_06_delete_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        self.assertNotIn("Updated Task", self.driver.page_source)

    def test_07_logout(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        self.assertIn("login.php", self.driver.current_url)

    def test_08_login_with_correct_credentials(self):
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys(type(self).password)
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_09_login_with_wrong_password(self):
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("Invalid password", self.driver.page_source)

    def test_10_login_with_nonexistent_user(self):
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "username").send_keys("notAUser")
        self.driver.find_element(By.NAME, "password").send_keys("something")
        self.driver.find_element(By.TAG_NAME, "button").click()
        self.assertIn("User not found", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
