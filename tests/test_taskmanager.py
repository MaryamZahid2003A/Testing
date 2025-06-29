import unittest
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from datetime import datetime

class NotesAppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.base_url = "http://localhost"
        cls.email = f"testuser{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        cls.password = "password"
        cls.username = "testuser1"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def login(self, email=None, password=None):
        self.driver.get(f"{self.base_url}/login.php")
        self.wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys(email or self.email)
        self.driver.find_element(By.NAME, "password").send_keys(password or self.password)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        self.wait.until(EC.url_contains("index.php"))

    def test_01_signup_user(self):
        self.driver.get(f"{self.base_url}/signup.php")
        self.wait.until(EC.visibility_of_element_located((By.NAME, "name"))).send_keys(self.username)
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Signup')]").click()
        self.wait.until(EC.url_contains("login.php"))
        self.assertIn("Login", self.driver.page_source)

    def test_02_login_user(self):
        self.login(email=self.email, password=self.password)
        self.assertIn("index.php", self.driver.current_url)

    def test_03_add_note(self):
        self.login()
        self.wait.until(EC.visibility_of_element_located((By.NAME, "title"))).send_keys("Test Note")
        self.driver.find_element(By.NAME, "description").send_keys("This is a test note.")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Note')]").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "note-card")))
        notes = self.driver.find_elements(By.CLASS_NAME, "note-card")
        found = any("Test Note" in note.text for note in notes)
        self.assertTrue(found)

    def test_04_edit_note(self):
        self.login()
        self.driver.find_element(By.NAME, "title").send_keys("Edit Me")
        self.driver.find_element(By.NAME, "description").send_keys("Before edit")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Note')]").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "note-card")))

        notes = self.driver.find_elements(By.CLASS_NAME, "note-card")
        for note in notes:
            if "Edit Me" in note.text:
                note.find_element(By.LINK_TEXT, "Edit").click()
                break

        title_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "title")))
        title_input.clear()
        title_input.send_keys("Edited Title")
        desc_input = self.driver.find_element(By.NAME, "description")
        desc_input.clear()
        desc_input.send_keys("Edited Description")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Update')]").click()
        self.wait.until(EC.url_contains("index.php"))
        self.assertIn("Edited Title", self.driver.page_source)

    def test_05_delete_note(self):
        self.login()
        self.driver.find_element(By.NAME, "title").send_keys("Delete Me")
        self.driver.find_element(By.NAME, "description").send_keys("Will be deleted")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Note')]").click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "note-card")))

        notes = self.driver.find_elements(By.CLASS_NAME, "note-card")
        for note in notes:
            if "Delete Me" in note.text:
                note.find_element(By.LINK_TEXT, "Delete").click()
                try:
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    pass
                break

        self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Me')]")))
        notes = self.driver.find_elements(By.CLASS_NAME, "note-card")
        self.assertFalse(any("Delete Me" in n.text for n in notes))

    def test_06_logout_user(self):
        self.login()
        logout_link = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
        logout_link.click()
        self.wait.until(EC.url_contains("login.php"))
        self.assertIn("login.php", self.driver.current_url)

    def test_07_prevent_empty_note_submission(self):
        self.login()
        self.driver.find_element(By.NAME, "title").clear()
        self.driver.find_element(By.NAME, "description").clear()
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Add Note')]").click()
        self.assertIn("index.php", self.driver.current_url)

    def test_08_login_with_wrong_password(self):
        self.driver.get(f"{self.base_url}/login.php")
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_09_duplicate_signup_should_fail(self):
        self.driver.get(f"{self.base_url}/signup.php")
        self.driver.find_element(By.NAME, "name").send_keys(self.username)
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//button[contains(text(),'Signup')]").click()
        self.assertTrue("already exists" in self.driver.page_source or "signup.php" in self.driver.current_url)

    def test_10_session_persistence_after_refresh(self):
        self.login()
        self.driver.refresh()
        time.sleep(2)
        self.assertIn("index.php", self.driver.current_url)

if __name__ == "__main__":
    unittest.main()
