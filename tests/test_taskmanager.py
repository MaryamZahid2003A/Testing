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

class TaskManagerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')  # Comment out for debugging visually
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        # Optional: Uncomment below line if using Chromium instead of Google Chrome
        # options.binary_location = "/usr/bin/chromium-browser"

        chrome_service = Service("/usr/bin/chromedriver")
        cls.driver = webdriver.Chrome(service=chrome_service, options=options)

        cls.driver.implicitly_wait(5)
        cls.base_url = "http://localhost"
        cls.username = ''.join(random.choices(string.ascii_lowercase, k=6))
        cls.password = "test123"

    def test_01_signup(self):
        self.driver.get(f"{self.base_url}/signup.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys(type(self).password)
        self.driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(self.driver, 10).until(lambda d: "index.php" in d.current_url)
        self.assertIn("index.php", self.driver.current_url)

    def test_02_add_task(self):
        self.driver.get(f"{self.base_url}/add.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "title")))
        self.driver.find_element(By.NAME, "title").send_keys("Test Task")
        self.driver.find_element(By.NAME, "description").send_keys("This is a test description.")
        self.driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(self.driver, 10).until(lambda d: "index.php" in d.current_url)
        self.assertIn("index.php", self.driver.current_url)

    def test_03_task_appears_on_dashboard(self):
        self.driver.get(f"{self.base_url}/index.php")
        tasks = self.driver.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any("Test Task" in t.text for t in tasks))

    def test_04_edit_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit")))
        self.driver.find_element(By.LINK_TEXT, "Edit").click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "title")))
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.clear()
        title_input.send_keys("Updated Task")
        self.driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(self.driver, 10).until(lambda d: "index.php" in d.current_url or "edit.php" in d.current_url)
        self.assertTrue("index.php" in self.driver.current_url or "edit.php" in self.driver.current_url)

    def test_05_verify_task_updated(self):
        self.driver.get(f"{self.base_url}/index.php")
        self.assertIn("Updated Task", self.driver.page_source)

    def test_06_delete_task(self):
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Delete")))
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        alert = self.driver.switch_to.alert
        alert.accept()

        WebDriverWait(self.driver, 5).until_not(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Updated Task"))
        self.assertNotIn("Updated Task", self.driver.page_source)

    def test_07_logout(self):
        self.driver.get(f"{self.base_url}/index.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        WebDriverWait(self.driver, 10).until(lambda d: "login.php" in d.current_url)
        self.assertIn("login.php", self.driver.current_url)

    def test_08_login_with_correct_credentials(self):
        self.driver.get(f"{self.base_url}/login.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys(type(self).password)
        self.driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(self.driver, 10).until(lambda d: "index.php" in d.current_url)
        self.assertIn("index.php", self.driver.current_url)

    def test_09_login_with_wrong_password(self):
        self.driver.get(f"{self.base_url}/logout.php")
        self.driver.get(f"{self.base_url}/login.php")
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").send_keys(type(self).username)
        self.driver.find_element(By.NAME, "password").send_keys("wrongpass")
        self.driver.find_element(By.TAG_NAME, "button").click()

        # Adjust message check according to your actual PHP implementation
        self.assertTrue("Invalid" in self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
