from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver


class SeleniumViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def test_flow(self):
        self.selenium.get(f"{self.live_server_url}/distribute/")
    
        # Add items.
        self.selenium.find_element(By.NAME, "user-item").send_keys("Transport belt")
        self.selenium.find_element(By.NAME, "user-count").send_keys("80")
        self.selenium.find_element(
            By.XPATH, "/html/body/main/article/section/form[1]/fieldset/p[3]/button"
        ).click()
        self.selenium.find_element(By.NAME, "user-item").send_keys("chemplant")
        self.selenium.find_element(By.NAME, "user-count").clear()
        self.selenium.find_element(By.NAME, "user-count").send_keys("6")
        self.selenium.find_element(By.NAME, "user-count").send_keys(Keys.RETURN)
        self.selenium.find_element(By.NAME, "user-count").clear()
        self.selenium.find_element(By.NAME, "user-count").send_keys("4")
        self.selenium.find_element(By.NAME, "user-item").send_keys("thruster")
        self.selenium.find_element(By.NAME, "user-item").send_keys(Keys.RETURN)
        self.selenium.find_element(By.NAME, "user-item").send_keys("car")
        self.selenium.find_element(By.NAME, "user-count").clear()
        self.selenium.find_element(By.NAME, "user-count").send_keys("1")
        self.selenium.find_element(
            By.XPATH, "/html/body/main/article/section/form[1]/fieldset/p[3]/button"
        ).click()

        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[4]/td[1]").text == "Transport belt"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[4]/td[2]").text == "80"
        # Increment item count.
        self.selenium.find_element(By.NAME, "user-item").send_keys("belt")
        self.selenium.find_element(By.NAME, "user-count").clear()
        self.selenium.find_element(By.NAME, "user-count").send_keys("5")
        self.selenium.find_element(By.NAME, "user-item").send_keys(Keys.RETURN)

        # Remove an item.
        self.selenium.find_element(By.CSS_SELECTOR, "#itemlist > tr:nth-child(1) > td:nth-child(3) > button:nth-child(1)").click()

        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[1]/td[1]").text == "Chemical plant"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[1]/td[2]").text == "6"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[2]/td[1]").text == "Thruster"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[2]/td[2]").text == "4"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[3]/td[1]").text == "Transport belt"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/article/aside/table/tbody/tr[3]/td[2]").text == "85"

        # Distribute and check results.
        self.selenium.find_element(By.NAME, "num-silos").send_keys("2")
        self.selenium.find_element(By.XPATH, "/html/body/main/article/section/form[2]/p[2]/button").click()

        assert self.selenium.find_element(By.XPATH, "/html/body/main/section[1]/p[1]").text == "Available silos: 2"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/section[1]/p[2]").text == "Required launches: 3"
        assert self.selenium.find_element(By.XPATH, "/html/body/main/section[1]/p[3]").text == "Required launch cycles: 2"
