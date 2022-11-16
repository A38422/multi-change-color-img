import os

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pathlib import Path

from selenium.webdriver import Chrome as Driver
from typing import Any
import json

import time

from yaml import load, dump

from selenium.webdriver.common.keys import Keys


def evaluationString(fun: str, *args: Any) -> str:
    """Convert function and arguments to str."""
    _args = ', '.join([
        json.dumps('undefined' if arg is None else arg) for arg in args
    ])
    expr = '(' + fun + ')(' + _args + ')'
    return expr


def evaluateOnNewDocument(driver: Driver, pagefunction: str, *args: str) -> None:
    js_code = evaluationString(pagefunction, *args)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js_code,
    })


def chrome_runtime(driver: Driver, run_on_insecure_origins: bool = False, **kwargs) -> None:
    evaluateOnNewDocument(
        driver, Path(__file__).parent.joinpath("config/js/chrome.runtime.js").read_text(),
        run_on_insecure_origins,
    )


def save_append_txt(file_name, data):
    with open(f"data_lazada\\{file_name}", 'a+', encoding="utf-8") as f:
        f.write(f"{data}\n")
        f.close()


def clear_logs(file_name):
    with open(file_name, 'w') as f:
        f.write('')
        f.close()


def generate_driver():
    options = Options()

    options = webdriver.ChromeOptions()

    options.add_argument('--profile-directory=Default')

    driver = webdriver.Chrome(executable_path='config/chromedriver.exe')

    return driver


def click(driver, xpath, send_key=None, sleep=1, control=False, send_key2=None):
    try:
        element = driver.find_elements(By.XPATH, xpath)
        if len(element) > 0:
            element[0].click()
            time.sleep(sleep)
            if send_key:
                if control and send_key2:
                    element[0].send_keys(Keys.CONTROL, send_key)
                    element[0].send_keys(send_key2)
                else:
                    element[0].send_keys(send_key)

    except Exception as e:
        print(e)
        pass
    return driver


def scroll_element(driver, xpath, sleep=0.0):
    try:
        element = driver.find_elements(By.XPATH, xpath)
        if len(element) > 0:
            action = ActionChains(driver)
            action.move_to_element(element[0])
            action.perform()
            time.sleep(sleep)
            action.release()
    except Exception as e:
        pass
    return driver


def login(driver, sleep=0.0):
    try:
        username = "thecryptobox.official.expert@gmail.com"
        password = "Hop@123456"

        driver = click(
            driver,
            xpath='//input[@name="identification"]',
            send_key=username
        )
        time.sleep(2)

        driver = click(
            driver,
            xpath='//input[@name="password"]',
            send_key=password
        )
        time.sleep(2)

        driver = click(
            driver,
            xpath='//button[@type="submit"]',
        )
        time.sleep(sleep)
    except Exception as e:
        pass
    return driver


def upload_svg(driver, svg, sleep=0.0):
    try:
        driver.find_elements(
            By.XPATH, "//article//span[@class='x-file-input']//input[@type='file']")[0]\
            .send_keys(f"{os.path.abspath(svg)}")
        time.sleep(sleep)
    except Exception as e:
        print(f'Loi upload {svg}')


def thecryptobox(url, path_svg):
    driver = generate_driver()
    try:
        driver.get(url)
        time.sleep(5)

        driver = login(driver, sleep=10)

        driver = scroll_element(driver, xpath='(//h3[@class="gh-content-entry-title"])[last()]', sleep=3)

        driver = scroll_element(driver, xpath='(//h3[@class="gh-content-entry-title"])[last()]', sleep=3)

        driver = scroll_element(driver, xpath='(//h3[@class="gh-content-entry-title"])[last()]', sleep=3)

        links = driver.find_elements(By.XPATH,
                                     '//ol[contains(@class,"posts-list")]//a[contains(@class,"gh-list-data")]')
        links = list(map(lambda x: x.get_attribute('href'), links))

        new_links = []
        for link in links:
            if link not in new_links:
                new_links.append(link)

        titles = driver.find_elements(By.XPATH, '//h3[@class="gh-content-entry-title"]')
        titles = list(map(lambda x: x.text.replace(' ', '')
                                          .replace('-', '')
                                          .replace('/', ''), titles))

        index = 0

        for link in new_links:
            driver.get(link)
            time.sleep(3)

            upload_svg(driver, f"{path_svg}\\{titles[index]}.svg", sleep=3)

            driver = click(driver,
                           xpath='//div[contains(@class,"gh-viewport")]//button[contains(@class,"green")]',
                           sleep=3)
            print(index)
            index += 1
            time.sleep(7)

        time.sleep(10)
        driver.quit()
    except Exception as e:
        if driver:
            driver.quit()
        print(e)


if __name__ == '__main__':
    thecryptobox(
        'https://thecryptobox-official.digitalpress.blog/ghost/#/posts?tag=candlestick-patterns',
        'candlestick-patterns1'
    )
    # thecryptobox(
    #     'https://thecryptobox-official.digitalpress.blog/ghost/#/posts?tag=technical-indicators',
    #     'mau'
    # )