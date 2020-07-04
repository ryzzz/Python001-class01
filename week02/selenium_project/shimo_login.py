from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

'''
使用WebDriver登录石墨笔记页面
'''
# --------------------------------------------------------------------------------
# 超时时间
TIMEOUT = 30
# 石墨笔记URL
URL = 'https://shimo.im/welcome'
# 石墨笔记用户名
USERNAME = 'test_username'
# 石墨笔记密码
PASSWORD = 'test_password'

# Xpath路径
LOGIN_BUTTON = '//button[@class="login-button btn_hover_style_8"]'
USERNAME_BOX = '//input[@name="mobileOrEmail"]'
PASSWORD_BOX = '//input[@name="password"]'
LOGIN_CONFIRM_BUTTON = '//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]'
# --------------------------------------------------------------------------------

driver = webdriver.Chrome()
driver.get(URL)


def click_login_button():
    locator = (By.XPATH, LOGIN_BUTTON)
    click_button(locator)


def click_login_confirm_button():
    locator = (By.XPATH, LOGIN_CONFIRM_BUTTON)
    click_button(locator)


def send_username():
    locator = (By.XPATH, USERNAME_BOX)
    input_text(locator, USERNAME)


def send_password():
    locator = (By.XPATH, PASSWORD_BOX)
    input_text(locator, PASSWORD)


def get_element(locator):
    try:
        element = driver.find_element(*locator)
    except Exception as e:
        raise e
    else:
        return element


def click_button(locator):
    try:
        wait_element_to_be_clickable(locator)
        element = get_element(locator)
        element.click()
    except Exception as e:
        raise e


def input_text(locator, text):
    try:
        wait_element_to_be_visible(locator)
        element = get_element(locator)
        element.send_keys(text)
    except Exception as e:
        raise e


def wait_element_to_be_clickable(locator):
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator))
    except Exception as e:
        raise e


def wait_element_to_be_visible(locator):
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(locator))
    except Exception as e:
        raise e


def run_login():
    click_login_button()
    send_username()
    send_password()
    click_login_confirm_button()


if __name__ == '__main__':
    run_login()
