# -*- coding: utf-8 -*-
# get模块，加入一定延迟防止请求过快

import requests
import time
from selenium import webdriver

def get_and_sleep(url, headers, proxies_dict,timeout=5,sleep_time=4):
    try:
        response = requests.get(url, headers=headers, proxies=proxies_dict, timeout=timeout)
        time.sleep(sleep_time)
        if response.status_code == 200:
            return response
        else:
            print(f"Error: {response.status_code}")
            return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    

def selenium_get(url, driver,sleep_time=4):
    try:
        driver.get(url)
        time.sleep(sleep_time)
        return driver.page_source
    except Exception as e:
        print(f"Selenium request failed: {e}")
        return None

if __name__ == "__main__":
    None