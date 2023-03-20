from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

class ExeScraper:
    def __init__(self):
        options = Options()
        options.add_argument("-profile")
        options.add_argument('/home/petru/.mozilla/firefox/t1p5qnqs.Selenium Downloader')
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        self.driver = webdriver.Firefox(capabilities=firefox_capabilities, options=options)

    def __del__(self):
        self.driver.quit()

    def scrape_page_of_exe(self, url):
        self.driver.get(url)
        app_icons = self.driver.find_elements(By.CLASS_NAME, 'appicon')
        for i in range(len(app_icons)):
            self.driver.implicitly_wait(5)
            app_icons[i].click()

            self.driver.implicitly_wait(5)
            dl_butt = self.driver.find_element(By.ID, 'sf-dlbutton')
            dl_butt.click()

            self.driver.implicitly_wait(5)
            main_dl_butt = self.driver.find_element(By.CLASS_NAME, 'main-dlink')
            main_dl_butt.click()

            self.driver.implicitly_wait(5)
            self.driver.back()
            self.driver.back()

            app_icons = self.driver.find_elements(By.CLASS_NAME, 'appicon')
    
    def run(self):
        base = 'https://www.snapfiles.com/new/list-whatsnew.html'
        for i in range(2, 16):
            url = base[:len(base)-5] + str(i) + '.html'
            self.scrape_page_of_exe(url)

inst  = ExeScraper()
inst.run()
