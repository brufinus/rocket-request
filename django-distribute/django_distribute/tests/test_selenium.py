from importlib.metadata import version as get_version

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@tag("slow", "selenium")
class SeleniumViewTests(StaticLiveServerTestCase):
    fixtures = ["items"]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def test_items_and_get_results(self):
        """Test the add/remove item flow and get results."""
        wait = WebDriverWait(self.selenium, 2)

        self.selenium.get(f"{self.live_server_url}/distribute/")

        # Add items.
        self.selenium.find_element(By.NAME, "user-item").send_keys("Transport belt")
        self.selenium.find_element(By.NAME, "user-count").send_keys("80")
        self.selenium.find_element(
            By.XPATH,
            "/html/body/main/article/section/form[1]/div/div/div[2]/button/div",
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
            By.XPATH,
            "/html/body/main/article/section/form[1]/div/div/div[2]/button/div",
        ).click()

        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[4]/td[2]",
            ).text
            == "Transport belt"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[4]/td[3]",
            ).text
            == "80"
        )
        # Increment item count.
        self.selenium.find_element(By.NAME, "user-item").send_keys("belt")
        self.selenium.find_element(By.NAME, "user-count").clear()
        self.selenium.find_element(By.NAME, "user-count").send_keys("5")
        self.selenium.find_element(By.NAME, "user-item").send_keys(Keys.RETURN)

        # Remove an item.
        remove_button = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/main/article/aside/div/div/table/tbody/tr[1]/td[1]/button/img",
                )
            )
        )
        remove_button.click()

        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[1]/td[2]",
            ).text
            == "Chemical plant"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[1]/td[3]",
            ).text
            == "6"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[2]/td[2]",
            ).text
            == "Thruster"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[2]/td[3]",
            ).text
            == "4"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[3]/td[2]",
            ).text
            == "Transport belt"
        )
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/article/aside/div/div/table/tbody/tr[3]/td[3]",
            ).text
            == "85"
        )

        assert (
            self.selenium.find_element(
                By.CSS_SELECTOR, "div.change-info:nth-child(4)"
            ).text
            == f"Rocket Request v{get_version("django-distribute")}"
        )

        # Distribute and check results.
        self.selenium.find_element(By.NAME, "num-silos").send_keys("2")
        self.selenium.find_element(
            By.XPATH, "/html/body/main/article/section/form[2]/p[2]/button"
        ).click()

        # Summary
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[1]/td[1]"
            ).text
            == "Available silos"
        )
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[1]/td[2]"
            ).text
            == "2"
        )
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[2]/td[1]"
            ).text
            == "Required launches"
        )
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[2]/td[2]"
            ).text
            == "3"
        )
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[3]/td[1]"
            ).text
            == "Required launch cycles"
        )
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/section/div/div/table/tbody/tr[3]/td[2]"
            ).text
            == "2"
        )

        # Per-cycle
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/div[1]/section[1]/h3[2]"
            )
        ).text == "Cycle 2 of 2"
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/div[1]/section[1]/div[2]/div/div/table/tbody/tr/td[1]",
            )
        ).text == "Transport belt"
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/div[1]/section[1]/div[2]/div/div/table/tbody/tr/td[2]",
            )
        ).text == "25"

        # Per-silo
        assert (
            self.selenium.find_element(
                By.XPATH, "/html/body/main/div[1]/section[2]/h3[2]"
            )
        ).text == "Silo 2 (1000 kg)"
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/div[1]/section[2]/div[1]/div/div/table/tbody/tr[3]/td[1]",
            )
        ).text == "Thruster"
        assert (
            self.selenium.find_element(
                By.XPATH,
                "/html/body/main/div[1]/section[2]/div[1]/div/div/table/tbody/tr[3]/td[2]",
            )
        ).text == "4"

        assert (
            self.selenium.find_element(
                By.CSS_SELECTOR, "div.change-info:nth-child(4)"
            ).text
            == f"Rocket Request v{get_version("django-distribute")}"
        )

    def test_contact_page(self):
        """Test elements on the contact page."""
        self.selenium.get(f"{self.live_server_url}/distribute/contact")
        assert (
            self.selenium.find_element(By.XPATH, "/html/body/main/section/h1")
        ).text == "Contact me"
        assert (
            self.selenium.find_element(By.XPATH, "/html/body/main/section/div/h2[1]")
        ).text == "Feedback"
        assert (
            self.selenium.find_element(By.XPATH, "/html/body/main/section/div/p[3]")
        ).text == "Have any other inquiries or comments? Send me an email."
        assert (
            self.selenium.find_element(
                By.CSS_SELECTOR, "div.change-info:nth-child(4)"
            ).text
            == f"Rocket Request v{get_version("django-distribute")}"
        )

    def test_about_page(self):
        """Test elements on the about page."""
        self.selenium.get(f"{self.live_server_url}/distribute/about")
        assert (
            self.selenium.find_element(By.XPATH, "/html/body/main/section/h1")
        ).text == "About"
        assert (
            self.selenium.find_element(By.XPATH, "/html/body/main/section/div/h2[1]")
        ).text == "Why?"
        assert (
            self.selenium.find_element(
                By.CSS_SELECTOR, "div.change-info:nth-child(4)"
            ).text
            == f"Rocket Request v{get_version("django-distribute")}"
        )

    def test_toggle_theme(self):
        """Tests the toggle theme button."""
        self.selenium.get(f"{self.live_server_url}/distribute/")
        self.selenium.find_element(By.ID, "theme-toggle").click()

    def test_navigation(self):
        """Tests navigation between pages using the nav bar."""
        self.selenium.get(f"{self.live_server_url}/distribute/")
        self.selenium.find_element(
            By.CSS_SELECTOR, ".nav-bar-item-context > div:nth-child(1)"
        ).click()
        assert self.selenium.current_url == f"{self.live_server_url}/distribute/"
        self.selenium.find_element(
            By.CSS_SELECTOR,
            ".links-list > li:nth-child(2) > a:nth-child(1) > div:nth-child(1)",
        ).click()
        assert (
            self.selenium.current_url == f"{self.live_server_url}/distribute/contact/"
        )
        self.selenium.find_element(
            By.CSS_SELECTOR, ".links-list > li:nth-child(3) > a:nth-child(1)"
        ).click()
        assert self.selenium.current_url == f"{self.live_server_url}/distribute/about/"
        self.selenium.find_element(
            By.CSS_SELECTOR, ".links-list > li:nth-child(1) > a:nth-child(1)"
        ).click()
        assert self.selenium.current_url == f"{self.live_server_url}/distribute/"
