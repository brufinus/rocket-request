from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from django_distribute.data.items import ITEMS


@tag("slow", "selenium")
class SeleniumViewTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        options = Options()
        options.add_argument("--headless=new")
        cls.selenium = WebDriver(options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def add_item(self, item: str, count: str, index: int):
        """Test helper method for adding items."""
        wait = WebDriverWait(self.selenium, 2)
        self.selenium.find_element(By.ID, "user-item-input").send_keys(item)
        count_input = self.selenium.find_element(By.ID, "user-count-input")
        count_input.clear()
        count_input.send_keys(count)
        count_input.send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child({index}) > .added-item")))

    def test_add_items(self):
        """Tests adding items to the itemlist."""
        wait = WebDriverWait(self.selenium, 2)
        self.selenium.get(f"{self.live_server_url}/")

        self.selenium.find_element(By.ID, "user-item-input").send_keys("Transport belt")
        self.selenium.find_element(By.ID, "user-count-input").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("80")
        self.selenium.find_element(By.CSS_SELECTOR, "#add-item-button > .text-button").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "tr:nth-child(1) > .added-item")))
        self.add_item("chemplant", "6", 2)
        self.add_item("TH_Ru sT-E r -_", "4", 3)

        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > .added-item").text, "Chemical plant")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(3)").text, "6")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .added-item").text, "Thruster")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(3)").text, "4")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > .added-item").text, "Transport belt")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > td:nth-child(3)").text, "80")

        self.selenium.find_element(By.CSS_SELECTOR, "#add-item-button > .text-button").click()
        self.add_item("tanpot bolt", "40", 3)

        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > td:nth-child(3)").text, "120")

    def test_remove_items(self):
        """Tests removing items from the itemlist."""
        wait = WebDriverWait(self.selenium, 2)
        self.selenium.get(f"{self.live_server_url}/")

        self.add_item("Transport belt", "1", 1)
        self.add_item("Car", "1", 2)

        self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .trash-icon").click()
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > .added-item").text, "Transport belt")
        self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .trash-icon").click()

    def test_distribute_results(self):
        """Tests item distribution and results."""
        self.selenium.get(f"{self.live_server_url}/")

        self.add_item("Inserter", "12", 1)
        self.add_item("Pipe", "17", 2)
        self.add_item("Crusher", "5", 3)
        self.add_item("Assembling machine 3", "21", 4)
        self.add_item("Asteroid collector", "16", 5)

        self.selenium.find_element(By.ID, "num-silos").click()
        self.selenium.find_element(By.ID, "num-silos").send_keys("2")
        self.selenium.find_element(By.ID, "distribute-button").click()
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "#summary tr:nth-child(1) > td:nth-child(2)").text, "2")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "#summary tr:nth-child(2) > td:nth-child(2)").text, "4")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "#summary tr:nth-child(3) > td:nth-child(2)").text, "2")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".distribute-results:nth-child(1) > h3:nth-child(4)").text, "Cycle 2 of 2")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".results-section-container:nth-child(5) > h4:nth-child(3)").text, "Silo 2")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".results-section-container:nth-child(5) > .item-results-container:nth-child(4) tr:nth-child(1) > td:nth-child(2)").text, "9")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".distribute-results:nth-child(2) > h3:nth-child(4)").text, "Silo 2 (1265 kg)")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".results-section-container:nth-child(5) tr:nth-child(4) > td:nth-child(1)").text, "Crusher")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".results-section-container:nth-child(5) tr:nth-child(4) > td:nth-child(2)").text, "4")

    def test_contact_page(self):
        """Tests elements on the contact page."""
        self.selenium.get(f"{self.live_server_url}/contact")
        assert (self.selenium.find_element(By.XPATH, "/html/body/main/section/h1")).text == "Contact me"
        assert (self.selenium.find_element(By.XPATH, "/html/body/main/section/div/h2[1]")).text == "Feedback"
        assert (self.selenium.find_element(By.XPATH, "/html/body/main/section/div/p[3]")).text == "Have any other inquiries or comments? Send me an email."

    def test_about_page(self):
        """Tests elements on the about page."""
        self.selenium.get(f"{self.live_server_url}/about")
        assert (self.selenium.find_element(By.XPATH, "/html/body/main/section/h1")).text == "About"
        assert (self.selenium.find_element(By.XPATH, "/html/body/main/section/div/h2[1]")).text == "Why?"

    def test_toggle_theme(self):
        """Tests the toggle theme button."""
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.ID, "theme-toggle").click()

    def test_navigation(self):
        """Tests navigation between pages using the nav bar."""
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.CSS_SELECTOR, ".nav-bar-item-context > div:nth-child(1)").click()
        assert self.selenium.current_url == f"{self.live_server_url}/"
        self.selenium.find_element(By.CSS_SELECTOR, ".links-list > li:nth-child(2) > a:nth-child(1) > div:nth-child(1)").click()
        assert self.selenium.current_url == f"{self.live_server_url}/contact/"
        self.selenium.find_element(By.CSS_SELECTOR, ".links-list > li:nth-child(3) > a:nth-child(1)").click()
        assert self.selenium.current_url == f"{self.live_server_url}/about/"
        self.selenium.find_element(By.CSS_SELECTOR, ".links-list > li:nth-child(1) > a:nth-child(1)").click()
        assert self.selenium.current_url == f"{self.live_server_url}/"

    def test_blueprint_import(self):
        """Tests the blueprint import functionality."""
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.ID, "blueprint-input").click()
        self.selenium.find_element(By.ID, "blueprint-input").send_keys(
            "0eNrtnW1uIzmShq/S0G9pkBHMz8bMAov9uzcYFAxZTrsSLUsefdROTcMH2IPsxfYkmynJUlY5qQzyqXbbvQ000CVZekUyyQh+PIz4dXK73NdPm2a1m/z86+Su3i42zdOuWa8mP0/+Y/40v13WP63vf9pt5l/qzbZZPfzUrFb15qen5XxV77aT6aRZrFfbyc9//3WybR5W82Wns/v6VLcC26f5op4t14v5QXE6Wc0fu/dX8/2XZjt5br+8uqv/OflZnj9NJ/Vq1+ya+qh1ePH1ZrV/vK037QfO333Yr2a7/WZT71q9p/W2ORb210krM9Pp5Gv7P5c9P09faahJI7km4UwSV0uRniWa1bbe7Nr3Burxl+yk4f6Stc1012zqxfED5YBmZtF0Z039XjMd0MzPmu2zX22f1pvd7LZe7q6W1qRc2JWTMOXS0g5JWNtW9tJKWGklMRRXwkorYi5uYNuKmpVD28EZ2uFK7xUdEk3NxQ3svpLZbNFZdMgKSMDwys7lS151gemktb67zXp5c1t/nn9p1pvuW4tms9g3u5tNPb+7+Txf3d10n2qL0NrW3WZfT8+feHn/+NHH9V1bouECB4za1F/g4Wd1Gbf71h9sHjbr9v/j1kYO6idfs97vnva7yZB8FWPKbEXXJMaYGbUlxvQYtWNGs1HaRZggo7R9ULtQ6SzCXhilc5PBuGov1D78stDilWbp0IGt9pGXB0o7+8ArQqUDxt1ZW6vfzzY7+2Ce5f4CDzeGC7HNl+YoB5rjZKmblcdQuzTCKVrrkUX4r4GHOiSdx0iXtmIXMU1y1H6r3nexH9unZbMbW30klmpXQes9rQZXWkHz68OzHlKRkGWjpySXAbpcrx5mXcPXdzN/qdTfA4empGnQDHrQVN03y/Zbx7X3y6L8LPpY7+bLZbOYzbfth9bN3Wzxeb/6pf2Nf+zn7SP/2q3p15vHdvHfdbvHp/lmvus63ORvk25lv9/WN+cf6LrZUB3SEC/paecswFh9b6tG55FpHu5yTm39RkMxLSwL4EvhikCfVa+6/aC7gfLdnX/hvtlsdzeXraBTedb/bO7q7/vPsWW2u3m3+yR58l3n+evkebCWccuFU23HnFAas1rQfNh4ZEnQzsxBZnS0Z2IRlStPeUj0YqLu26c0M7Ss+IvdbRaMjqfMRaydjLVJY6Rzk3T2bUP5H8GVMqcjBrfZrFez9ab+oRY2y60l//7J/g5lvViyxWa//XzdSZavWrf9d/PkcV2dXrN6mLx86mag2M2ufjzV965nxer7+2bR1KvF11lrhvfLeqaHXezjp7vGuWlWX9q6rDdfT611ftWWqrV0i1/ajtFVePAv8vzpuf1voD3K8PXf0LAckq6s3SING4R5EmpSUpNF8Zru3GIYP7r3yy+G+qK3Xi7bSqyve/tsqE1/dIVPz+hLs9ntDyPpZWlw+MTs37+t9fd1/re2zt2w3O6XXUc8j5DVfrlsP9o12+xoOoZt0XA7Dw2o3AXt4mo++CzSME+cmg5eshjflZlGZB4jnZqki/ANxaEeOSRdhm8oWqWrwIXZlWc5+ANFYupm7lovKyxmLfXXfPAMTiP8STY8yS1chFbq0UqDrNsV45b+/7VtRRa3Z+f8e3b+WXyRx+yWqsWmFBebMl8s9o/75XzYx+UvFfAstY+lD3qSg53zYojqrkdu2mnl/X6zmi/qq6u6Y7u+tyllEWr7eo7MmYxfGXM4pqZz7lJipE29rtQId2MrtAvakHQm5CGNKK2tHbKA3v7eO3uZR/goHfZRZWHY8M6/aY4Xu35uiLv64Cg2+8MDmHU01eogY1hCT1/s2dOmtW/HD2+ah89dXQ5ro/4flvX9oNkuy/CjOW+DVFHbrs60H1dFHPT5ClpFneyJCRPSGOnEJO0C3aAM1j2Nc17JuxzPVRbvvGynwFXUWsnWV4qwZaNYHEFVxpTX1gHjV0liA4CSJMKLmdpaEglyuomN3IuZIyS28root/s+h6kkaYTflWHrLUkWIZb4xPIIB+gVKyLEvNUsIzyeV6yKEPNVU5IIJyeVDVyN8c1S2rQ1zINKNVz9mAMra/VjTqys1c+C/M1r1UEbGICwBjdGEetwxIbViETsKVpbuwq3UuKBTySAL82+KeegmIRbKb+YRoh5q+nCrZRfLI0Q81YzizFLpvMx0ZitM8lt2oF7Z1IMVz9uy+vUAO9uOhIApPasrO1p9ojU0CXJ618YtlouZtfL2GF6EKnFzha2mx0RLLi1uSM2vqxNEbXz9V77vIvY+jrUZVAsgkOX3CcWsQflL1kEa+4tWRqx6eQtWSoRYt6Sxewziel0WFIXo53+jpeSetCozct5GjWL83Lp+xzxPVDV5H1MJ8aSxtzbtPa8Mt53psb7gFGu38Q+SJZEr1dsnIJkQbtYktouMkbsYhkfaBbj+I2NnUZ553c6VrOIPS3xgBiSxbj61CcWsaflL1mMq/eWLGJPy1uyPMbVp29J9UuPawzhOcRF3MGSXIPuEIi+HUXpu4YSB1JKHniuJr8xXiJ51B6gLS5AHrgHaLsKHwUUitpKXES4EGNjlNH+2hh9IK8iCm9rlyJmS9B5rF+PLRxlGU7lew0f+BgDKWL2CL1FdTGUgThjkIAiDYHHP7DZ69GBYQC5JEMAeTzQ6K3X4ESpxxkGrdHkfc77iiJ+xWM8VC/KiPgRYgzZUUQtp6zxQIJu7oqJj5AyIjSO2BiDGGTQ3BZRPMB77fZlBA8gvrPtMmbt5Dvb7hGCQeT56+eYvp1R7KGIISuDMgb0lh4yOHJR7GJOfGd0pfnS2cV6+LSqiAmRV0vCtXxHhwFIYOp9MunbLTMrFz5bK0PvlP3QAqcxM8LShJ1KFXPwazu6qmLOfW1HVz20cLtezjezp/mqXl4LFuI7tejxhPPttn68XTbtNOVxvvjcrDp/ceU2/LEVzldw22ltPd88tt99mP+r/fKHungrPfjR1g7JH7EZNAm6yDYIE2gSYVxN58za4zH9y9jeQBrUcOHmuvBppeGm1KuVhW9QeusYEcLEW64iwoqZTg80gIC8SKc26SrUQHp2odUUvvMyE8p8MhIUtNQroxGLPdMxkUZhj0bpCIgjfZMpkgy3chZ+y9nYEpYzWw0bRmK5qHReMr5uVftOnwbwlBrYMBE4pW+QBNCUqbepB0sZgFamYQYrgLMsxkxWDGbpbcs05sKTrcoxU29nk84DlgypX3t8AaEBITu/aZ9BrYgrAc6nVUW0runuirqo+wE2aQn1255dI+2BjleVsn7dB4UiRpNXK4ZZ9mlFXf+XmD7uIlayv2MQa3Why2NvG/eDXnZJDp6W8919u3qbfd7f+qJDJofl4D/29XZ3CYD162R7bIhvw2sdl2iHf+tIAK7jtvC6XVeu6l2zmG0PK8S2SN2SznKjuHtjfzhESpKki9A1bwv0pZW+ny+3da8k7vs/fepVqC3Bze3+/r4X1uv8x8dm2+WOuOlfer55nLd1alodbxQwdVWEuZaY3U3tIZ/2zSRjBHKNQECTt0RMNA2iPt7w8HMx39yuVz/q8FN7iGtgTLKoOUCaBk8LbVOkNAs4rf7AjyuPO6tO//ihzrwtPbh9l1od30s39E37e6TudSEZEzJuxIzp9NjbqzpjFesRtiHnf+kfPu5UWEfrMcUBk888ymVnEfcVbPvJIfFj8zDlLDygu1E5Igy9UbkID4lsVA7Y6HVhyhF8ik05ABg+G0GjsgTvLhqFw/kUo7ALTshiFA5P32QUDmdGjMJ58FTPKBy+j+Q7ssnLiDVObjov1zz8/p2t/kUSsjQpQ3Mb+Nzbj4xmraYQnmd77wFKtDDuXJ1NZeUTciFHV8FNOhip8se2pwXWTcaaMwvImlHZ+moeu7ysomZAhSWSVBb7HN8i7YcWZcBK1vso7TjZeetGxkPbH23Dj61vj231RrY/zykl+SCLixPjMmBMP2K0fQ0JL5p/26HGdm4CWOHzNN1IfGvpwhcXZu00fKpu1s5iMroMqVuMZo/09Y/A5IOOwO9978ccfkUIE+Pjw7UsA2YJfpWQMwhT3/RPogNQ5tAxVklA7uq21w9qhEeNt13O0CocvrMqpwYIJj3V2mTBA8jgQN9QmTP0hMxifpMEPVoZMvR81GnMHyRpkFYRHKXtCq1WERSJ7YKrCwgGe5l8OZt0zLzOWGoNPGHxXXR1PRB58bl+bBZt/+0ChF/bYDzV/12PqmZRzx7btv5ow8j1aO6xB/Ln83iL55GFHfn5R1p4DGCroQnftLUqh0dSsVqw8LAqRmWJseiZTToibLBVOiKtti2GkZOIk0urdBp6sTzzNosnPfpl+D11luTKysxz2O56tPuwxLhC6P15fy3TQf1w4tbarcIPSozKAXh7YH/VcH7NqhwzyAqbtIuQzm3SEfC7tdQR8Lu11GOj7jI39Zwguh7UPjo3VW/p2tZ7bDabblJymvy853nS7nO7+Gttyux+f5hlfKCZUu/ewJip9j7xyizhuXXoetcCRqy9rxA9+n9EwVsGNXdcf799vxTh91212wZu/nXwgx+ou/ZuVAw/5lH7FHGPwmg8Xfg1XKPFdxGrEKNyeAhHa2vE7CxVNunKsvl/Lq/nSNilEXeRbBkeXI/mD51i29JTuB6OP+apK1/9nVnC24RphLOv/nT2v5P1TO3rMm+nyc0S3k5TWF21txClVcFbhirc2Vd/Ovu37a5ZYnX2vo6SSewegCnDkcvUWkJfR8zCr4gavWQWMdGxebfMgsWNut8s4maoLaOfyyICj9iS77mstDpNX8I1l1WxkwNjskSX20LxnMIW6+BRvsvFXFPPnWWXq9VZeBsrd2YJbylSo7fwFyKzKnjLkEcaIltqT5cXRkPkr2NpVfDWMfx0wDiei/AI7MbhXNiYl6sDpQ9dt85t/lDPWu/8y5UliS1xtyvME3RfOmNXREzQXyf//nOC/kYznsI8QVffiWVhnqD7O00RPDlW/XNy/MZdxWyvvY+5MtqtfKzPlWMT9cssy3daV47ONnRUwmqHk1GlMcM7XpaxOcd4g/R2E089dWhmeBTxbXaWublVvRLfzixmu/XsyLdeE/PtsZeltWG9xanMxRktTZ+l9TbxSHkqe7/1LVIrjWhh20qtD816a5iMFC+1PjOvQhb+zAbq96m1iq0/6qzs0RIv1619X3fRZrrX6sreJzq99rvrzd3xs609PepM7vfLh9Y6tL/9X/O+wzl+7uRi5svlzSk0zfZm2351e9/Ud2cYtr55+Vxbia7Kp5cnLzb8uYNvGo2P8SoI7Dc+Lf3Op/3vf//P5OQgLjVczfdfmu1vUsHOsd0cYwGBOl6NR3TVh/9t8vwemrtzym3ztt/tGvXvkk916oqpfpqe/i2Hf3f/m6bH99Pu/fz4frsu1mlxfL+doeu0dTiHfxeXf3e5FnXaJVs6qibdq+7Dh1fd37oQU4dXVSfXBefuXnURM+XwN+leue5nu+A9h79135h211t6r9JvXmXHEnbxiLq/ZcdXZdL/XnnQrIreqw5JPdS4+/+04yF7r7Q4veqq2p2zHl517067E4TDq+7dabcte3iVHj55qu3h3ak7tFfb6rvmZfy/ulR0CmuXP/tCb913Vuc4TLpu9Mq6UgGBAgn8Pv193AAvjyCjjyCjjyCDjyCDjyCDjyCjjyCljyCljyCFjyCFjyCFjyC6AU7psJyLFcioQEoFHBVQKiBQIIHfp79PG4A+AdoFcB98GQVKR4HSUaB0FCgdBUpHgcJRoHAUKBwFCkeBwlGgcBREP8DyJCCxAgUVyKlARgVSKuCogFIBgQIJ/D79fdoA9AnQLkD7IB0EeBS+2IGE2oGE2oGE2oGE2oGE2oGE2oGE2oEE2oEE2oEE2oEE2oEE2oEE2oEE2oEE2oEE2gGtoB2IF8ipQEYFUirgqIBSAYECCfw+/X3aAPQJ0C5A+yAdBHgUvtiBktqBktqBktqBktqBktqBktqBktqBEtqBEtqBEtqBEtqBEtqBEtqBEtqBEtqBktqBgtqBgtqBgtqBgtqBgtqBgtqBgtqBAtqBAtqBAtqBAtqBAtqBAtqBAtqBAtqBgtqBnNqBnNqBnNqBnNoBevyslABQSgAoJAAUEgAKCYDo79MnQLsA7YN0EOBR+GIHMmoHMmoHMmoHMmoHKAOhFENRiqEoxFAUYigKMZTo79MnQLsA7YN0EOBR+GIHUmoHKMUSL5BRgZQKOCqgVECgQAK/T3+fNgB9ArQL0D5IBwEehS92wFE7QDkepTSbUppNKc2mlGZTSrMppNkU0mwKaTaFNJtCmk0hzRb9fToI8Ch8sQNK7YBSO0B5PqU8n1KeTynPp5TnU8jzKeT5FPJ8Cnk+hTyfQp4v+vt0EOBR+GIHKE+olCdUyhMq5QmV8oRKeUKlPKFCnlAhT6iQJ1TIEyrkCRXyhAp5QoU8oVKeUClPqJQnVMoTKuUJlfKESnlCpTyhQp5QIU+okCdUyBMq5AkV8oQKeUKFPKFSnlAoTyiUJxTKEwrlCYXyhEJ5QqE8oUCeUCBPKJAnFMgTCuQJBfKEAnlCgTyhUJ5QKE8olCcUyhMK5QmF8oRCeUKhPKFAnlAgTyiQJxTIEwrkCQXyhAJ5QoE8oVCeUChPKJQnFMoTCuUJhfKEQnlCoTyhQJ5QIE8okCcUyBMK5AkF8oQCeUKBPKFQnlAoTyiUJxTKEwrlCYXyhEJ5QqE8oUCeUCBPKJAnFMgTCuQJBfKEAnlCgTyhUJ5QKE8olCcUyhMK5QmF8oRCeUKhPKFAnlAgTyiQJxTIEwrkCQXyhAJ5QoE8oVCeUChPKJQnFMoTCuUJhfKEQnlCoTyhQJ5QIE8okCcUyBMK5AkF8oQCeUKBPKFQnlAoTyiUJxTKEwrlCYXyhEJ5QqE8oUCeUCBPKJAnFMgTCuQJBfKEAnlCgTyhUJ5QKE8olCcUyhMK5QmF8oRCeUKhPKFAnlAgTyiQJxTIEwrkCQXyhAJ5QoE8oVCeUChPKJQnFMoTCuUJhfKEQnlCoTyhQJ5QIE8okCcUyBMK5AkF8oQCeUKBPKFQnlAoTyiUJxTKEwrlCYXyhEJ5QqE8oUCeUCBPKJAnFMgTCuQJBfKEAnlCgTyhUJ6Q4oSUJqQwIWUJKUpISUIKEkKOEGKEkCKEECFkCCFCCAlCCBBSfpDig5QepPAgZQcpOkjJQQoOQm4QYoOQGoTQIGQGITIIiUEIDFJekOKClBaksCBlBSkqSElBCgpCThBigpAShJAgZAQhIggJQQgIUj6Q4oGUDqRwIGUDKRpIyUAKBkIuEGKBkAqEUCBkAiESCIlACARSHpDigJQGpDAgZQEpCkhJQAoCQg4QYoCQAoQQIGQAIQIICUAIAFL+j+J/lP6j8B9l/yj6R8k/Cv5B7g9if5D6g9AfZP4g8geJPwj8Ud6P4n44CyhNOkZzjtGUYzTjGE04BvONwXRjMNsYTDYGc43BVGMw0xhMNEbjA9HwQDQ6EA0ORGMD0dBANDIQDQwE4wLBsEAwKhAMCgRjAsGQQDAiEAwIRDkeivFQiodCPJThoQgPJXgowAP5HYjvQHoHwjuQ3YHoDiR3ILjDxj2k9yC7B8k9yO1Bag8ye5DYY7weo/UYq8dIPcbpMUqPMXqM0IN8HnTv0LtD5w59O3Tt0LNDx878OnPrzKszp858OnPpzKMzhw79OVy+w9U7XLzDtTtcusOVO1y4s3U7W7azVTtbtLM1O1uysxU7W7DD9Trcnoe783BzHu7Nw615uDMPN+bZvjzblme78mxTnu3Jsy15tiPPNuThfjw8foen7/DwHZ69w6N3ePIOD97ZuTs7dmen7uzQnZ25syN3duLODtzheTvE6yBdB+E6yNZBtA6SdRCsY1wdw+oYVcegOsbUMaSOEXUMqIM8HcTnIT0P4XnIzkN0HpLzEJxn3DzD5hk1z6B5xswzZJ4R8wyYh7w8vB4Hb8fBy3Hwbhy8GgdvxsGLcexeHLsWx27FsUtx7E4cuxLHbsSxC3HwPhy8/g5vv8PL7/DuO7z6Dm++w4vv7N47u/bObr2zS+/szju78s5uvLML7/C+OwxvA6PbwOA2MLYNDG0DI9vAwDYsrg0La8Oi2rCgNiymDQtpwyLasIA2MJ4NDWdHo9nRYHY0lh0NZUcj2dFAdjCOHQxjB6PYwSB2MIYdDGEHI9jBAHY0fh0NZ0uj2dJgtjSWLQ1lSyPZ0kC2MI4tDGMLo9jCILYwhi0MYQsj2MIAtjR+LQ1nT6PZ02D2NJY9DWVPI9nTQPYwjj0MYw+j2MMg9jCGPQxhDyPYwwD2NH49TWdDs9nQZDY0lw1NZUMz2dBENjCPDUxjA7PYwCQ2MIcNTGEDM9jABDY0fw1NZ0ez2dFkdjSXHU1lRzPZ0UR2MI8dTGMHs9jBJHYwhx1MYQcz2MEEdjR/HU1nS7PZ0mS2NJctTWVLM9nSRLYwjy1MYwuz2MIktjCHLUxhCzPYwgS2NH8tTWdPs9nTZPY0lz1NZU8z2dNE9jCPPUxjD7PYwyT2MIc9TGEPM9jDBPY0f71AAE8ggScQwRPI4AmE8ARSeAIxPGEcnjAQTxiJJwzFE8biCYPxhNF4wnA8gTyeQCBPIJEnEMkTyOQJhPIEUnkCsTxhXJ4wME8YmScMzRPG5gmD84TRecLwPIF8nkBATyChJxDRE8joCYT0BFJ6AjE9YZyeMFBPGKknDNUTxuoJg/WE0XrCcD2BvJ5CXk8hr6eQ11PI6ynk9RTyegp5PWW8njJeTxmvp4zXU8brKeP1lPF6yng9hbyeQl5PIa+nkNdTyOsp5PUU8noKeT1lvJ4yXk8Zr6eM11PG6ynj9ZTxesp4PaXx7WiAOxrhjoa4ozHuaJA7GuWOhrmDce5goDsY6Q6GuoOx7mCwOxjtDoa7g7yeQl5PIa+nkNdTyOsp5PUU8noKeT1lvJ4yXk8Zr6eM11PG6ynj9ZTxesp4PYW8nkJeTyGvp5DXU8jrKeT1FPJ6Cnk9ZbyeMl5PGa+njNdTxusp4/WU8XrKeD2FvJ5CXk8hr6eQ11PI6ynk9RTyegp5PWW8njJeTxmvp4zXU8brKeP1lPF6yng9PG4hb6eQt1PI2ynk7RTydgp5O2W8nTLeThlvp4y3U8bbKePtlPF2CkFXhcCbQuBNIfCmEHhTCLwpBN6UAW/KgDdlwJsy4E0Z8KYMeFMGvCkkTRUSZwqJM4XEmULiTCFxppA4U0acKSPOlBFnyogzZcSZMuJMGXGmEPVUiHwpRL4UIl8KkS+FyJdC5EsZ8qUM+VKGfClDvpQhX8qQL2XIF+04DjJDjjFDjjFDDhJTDpITjpETjpETxq9/mk6aXf3Yfuh2ua+fNs1qN5lOlvPbetm+95/r1cPtumnf+VJvtoefyHKt0qrKSk2yNJXn5/8DcPItDQ=="
        )
        self.selenium.find_element(By.CSS_SELECTOR, "#import-button > .text-button").click()
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > .added-item").text, "Accumulator")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(3)").text, "6")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(19) > .added-item").text, "Underground belt")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(19) > td:nth-child(3)").text, "18")

    def test_blueprint_export(self):
        """Tests the blueprint export functionality."""
        self.selenium.get(f"{self.live_server_url}/")
        self.add_item("Transport belt", "1", 1)
        self.selenium.find_element(By.ID, "num-silos").click()
        self.selenium.find_element(By.ID, "num-silos").send_keys("1")
        self.selenium.find_element(By.ID, "distribute-button").click()
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, ".blueprint-box").text, "0eNqNUk1rwzAM/StGZ6ekpR1rYJfBDrt2xzGC42itqWOntlNWSv77ZKdpNvZBT7alp6enJ5+h0h22TplQVtbuoThPEQ/F65dnzClpzRD2amuEjjEjGoQCHB469AFdJnd0Qs9BmRo/oJj3bxzQBBUUDsXpcSpN11ToCMD/IuHQWk911sROxJXPcg6ndFKDC7x8V5pqfMR4lBE+9BkFcLgivkUvXYMTxrfWhaxCHZseOqFJIKWMdQ2NyUHaphVOBEt64SEFuugJDRfHIwq/K40N5ThCDUVwHfYxqwI2VDZZyUEL6kWxOd2PpCyNuLpbrJfr9ep+ka+Wy/lkYR5ZavTSqXZwAx6va2JbNEjSsGbViW2s3GNgm0HGjD0JuWPJTSatc0iDmtqzYJlgXmk7IwHTWidvfi44EWexBvqeX7ELfsNn+M2FLP24yYoXYmbPBBrFe0oKWucRy9GHf8zqPwGWVfPY")
        self.selenium.find_element(By.CSS_SELECTOR, "#copy-button > .text-button").click()

    def test_paste(self):
        """Tests the paste functionality."""
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.CSS_SELECTOR, "#paste-button > .text-button").click()

    def test_item_menu_flow(self):
        """Tests the add item flow using the item menu."""
        wait = WebDriverWait(self.selenium, 2)
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-1 > .menu-row:nth-child(2) > .menu-item:nth-child(1) > img").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("10")
        self.selenium.find_element(By.ID, "user-count-input").send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child(1) > .added-item")))
        self.selenium.find_element(By.CSS_SELECTOR, ".menu-header-item:nth-child(4) > img").click()
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-2 > .menu-row:nth-child(6) > .menu-item:nth-child(5) > img").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("6")
        self.selenium.find_element(By.ID, "user-count-input").send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child(2) > .added-item")))
        self.selenium.find_element(By.CSS_SELECTOR, ".menu-header-item:nth-child(6) > img").click()
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-3 > .menu-row:nth-child(9) > .menu-item:nth-child(4) > img").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("100")
        self.selenium.find_element(By.ID, "user-count-input").send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child(3) > .added-item")))
        self.selenium.find_element(By.CSS_SELECTOR, ".menu-header-item:nth-child(8) > img").click()
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-4 .menu-item:nth-child(5) > img").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("2")
        self.selenium.find_element(By.ID, "user-count-input").send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child(4) > .added-item")))
        self.selenium.find_element(By.CSS_SELECTOR, ".menu-header-item:nth-child(10) > img").click()
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-5 > .menu-row:nth-child(1) > .menu-item:nth-child(1) > img").click()
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-5 > .menu-row:nth-child(2) > .menu-item:nth-child(6) > img").click()
        self.selenium.find_element(By.ID, "user-count-input").send_keys("4")
        self.selenium.find_element(By.ID, "user-count-input").send_keys(Keys.ENTER)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"tr:nth-child(5) > .added-item")))

        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > .added-item").text, "Cannon shell")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(3)").text, "4")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .added-item").text, "Chemical plant")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(3)").text, "6")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > .added-item").text, "Jellynut")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > td:nth-child(3)").text, "100")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(4) > .added-item").text, "Thruster")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(4) > td:nth-child(3)").text, "2")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(5) > .added-item").text, "Transport belt")
        self.assertEqual(self.selenium.find_element(By.CSS_SELECTOR, "tr:nth-child(5) > td:nth-child(3)").text, "10")


@tag("slow", "selenium")
class SeleniumValidationTests(StaticLiveServerTestCase):
    """Selenium tests for data validation. Does not implicitly wait."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        options = Options()
        options.add_argument("--headless=new")
        cls.selenium = WebDriver(options)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.selenium.quit()
        super().tearDownClass()

    def test_validate_item_menu(self):
        """Validates the item menu options."""
        self.selenium.get(f"{self.live_server_url}/")
        self.selenium.find_element(By.CSS_SELECTOR, "#menu-contents-1 > .menu-row:nth-child(1) > .menu-item:nth-child(1) > img").click()
        self.assertIn(self.selenium.find_element(By.ID, "user-item-input").get_attribute("value"), ITEMS)

        menu = 1
        for k in range(4, 13, 2):
            for i in range(1, 13):
                for j in range(1, 11):
                    try:
                        self.selenium.find_element(By.CSS_SELECTOR, f"#menu-contents-{menu} > .menu-row:nth-child({i}) > .menu-item:nth-child({j}) > img").click()
                        self.assertIn(self.selenium.find_element(By.ID, "user-item-input").get_attribute("value"), ITEMS)
                    except NoSuchElementException:
                        pass
            if k > 10:
                break
            menu += 1
            self.selenium.find_element(By.CSS_SELECTOR, f".menu-header-item:nth-child({k}) > img").click()
