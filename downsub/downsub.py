from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import downsub.constants as const

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Downsub(webdriver.Edge):
    def __init__(self, playlist_link) -> None:
        super(Downsub, self).__init__()
        self.implicitly_wait(10)
        self.maximize_window()
        self.playlist_link = playlist_link

    def click_submit(self) -> int:
        """
        click submit button for deliver youtube link
        return (1=fail, 0=success)
        """
        try:
            self.find_element(
                by=By.CSS_SELECTOR,
                value='button[type="submit"]'
            ).click()
            print("submit found!")
            return 1
        except:
            print("submit element hidden by ad")
            return 0

    def close_wrapping_ad(self):
        """
        close an ad that hiding submit youtube link button if available
        """
        try:
            hide_ad_button = WebDriverWait(self, 5).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(text(), 'Hide')]"
                    )
                )
            )

            hide_ad_button.click()
            print("ad closed successfully")
        except:
            print("there is no ad")

    def download_subtitles(self, playlist: WebElement):
        """
        clicking download srt subtitle on current page
        """
        self.scroll_screen(playlist)
        # finding each playlist section
        playlist.click()

        try:
            # clicking each srt button
            WebDriverWait(self, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[contains(text(), 'SRT')]"
                    ),
                )
            ).click()
        except:
            print("subtitle not found")
            return

    def land_first_page(self):
        self.get(const.BASE_URL)

        text_edit = WebDriverWait(self, 30).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    'input'
                )
            )
        )
        text_edit.send_keys(self.playlist_link)

        print("close ad wrapping submit button...")
        self.close_wrapping_ad()

        if self.click_submit():
            print("download button clicked!")

    def check_pagination(self):
        """
        return int, (1=success, 0=fail) 
        """
        print("searching pagination...")
        try:
            # Locating pagination section on page
            next_button = WebDriverWait(self, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[contains(text(), 'navigate_next')]"
                    )
                )
            )

            # scroll to pagination section
            self.execute_script(
                "arguments[0].scrollIntoView();", next_button)

            next_button.click()
            print("pagination found!")
            time.sleep(2)
            return 1
        except Exception as e:
            print(f"error: {e}")
            print("pagination not found")
            return 0

    def scroll_screen(self, element):
        # scroll to the element
        self.execute_script(
            "arguments[0].scrollIntoView();",
            element
        )
        self.execute_script("window.scrollBy(0, -180);")

    def find_playlist_section(self):
        playlist = self.find_elements(
            by=By.CSS_SELECTOR,
            value=".pt-0.pb-0.col.col-12"
        )
        return playlist
