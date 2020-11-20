import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from chromedriver import setup_chrome
from env import FACEBOOK_EMAIL, FACEBOOK_PASSWORD

xpath_content = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]/div[1]/div/div/span'
xpath_like_count = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div/span[2]/span/span'
xpath_comment_count = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[1]/div/span'
xpath_share_count = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[2]/div[2]/span/div/span'
xpath_date_substrings = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a/span/span/span[2]/span'
xpath_see_more = '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[%d]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span/div/div/div'


def crawl(webdriver: WebDriver):
    index = 2
    while True:
        try:
            content_element = webdriver.find_element_by_xpath(xpath_content % index)
            ActionChains(driver).move_to_element(content_element).perform()
            if str(content_element.text).endswith('See More'):
                see_more_link_text = content_element.find_element_by_xpath(xpath_see_more % index)
                see_more_link_text.click()
            # content_element = webdriver.find_element_by_xpath(xpath_content % index) # reload
            print(content_element.text)

            date_elements = webdriver.find_elements_by_xpath(xpath_date_substrings % index)
            date_string = ''
            for date_element in date_elements:
                if date_element.get_attribute('style') != 'position: absolute; top: 3em;':
                    date_string += date_element.text
            date = date_string

            try:
                like_count_element = webdriver.find_element_by_xpath(xpath_like_count % index)
                like_count = like_count_element.text
                ActionChains(driver).move_to_element(like_count_element).perform()
            except:
                like_count = 0

            try:
                comment_count_element = webdriver.find_element_by_xpath(xpath_comment_count % index)
                comment_count = comment_count_element.text
                ActionChains(driver).move_to_element(comment_count_element).perform()
            except:
                comment_count = 0

            try:
                share_count_element = webdriver.find_element_by_xpath(xpath_share_count % index)
                share_count = share_count_element.text
                ActionChains(driver).move_to_element(share_count_element).perform()
            except:
                share_count = 0

            print('[Date] %s [Likes] %s [Comments] %s [Shares] %s' % (date, like_count, comment_count, share_count))

        except Exception as e:
            print(e)
            return

        index += 1
        time.sleep(3)


def login(webdriver: WebDriver):
    email_input_element = webdriver.find_element(by=By.ID, value='email')
    email_input_element.send_keys(FACEBOOK_EMAIL)
    password_input_element = webdriver.find_element(by=By.ID, value='pass')
    password_input_element.send_keys(FACEBOOK_PASSWORD)
    login_button_element = webdriver.find_element(by=By.NAME, value='login')
    login_button_element.click()
    time.sleep(1)
    return webdriver


def get_site(webdriver: WebDriver):
    webdriver.get('https://facebook.com/creatrip.tw')


if __name__ == '__main__':
    driver = setup_chrome()
    driver.get('https://facebook.com')
    driver = login(driver)

    while not str(driver.current_url).endswith('facebook.com/'):
        print('waiting approvement (%s)' % driver.current_url)
        time.sleep(3)

    get_site(driver)
    time.sleep(5)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()  # close to asking permission check
    crawl(driver)
