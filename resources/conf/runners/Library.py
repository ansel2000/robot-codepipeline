import json
import csv
import os
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
se2lib = BuiltIn().get_library_instance('SeleniumLibrary')

user_data = '../../data/user.csv'
product_data = '../../data/product.csv'
from browserstack_sdk import BrowserStackSdk

def get_url():
    print(BrowserStackSdk.get_current_platform()["customVariables"]["url"])
    return BrowserStackSdk.get_current_platform()["customVariables"]["url"]

def combine_dict(dict1, dict2):
    dict_1 = json.loads(str(dict1))
    dict_2 = json.loads(str(dict2))

    dict_1.update(dict_2)

    return dict_1


def get_row_item_from_file(filepath, key):

    dirname = os.path.dirname(__file__)
    filename = os.path.normpath(os.path.join(dirname, filepath))

    with open(filename, 'r') as data:
        for line in csv.reader(data):
            if line[0] == key:
                return line[1]


def get_password(username):

    password = get_row_item_from_file(user_data, username)
    return password


def get_product_prices():
    dirname = os.path.dirname(__file__)
    filename = os.path.normpath(os.path.join(
        dirname, product_data))

    prices = []
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            if line[3] != 'price':
                prices.append(int(line[3]))

    prices = sorted(prices)

    for i in range(0, len(prices)):
        prices[i] = str('$' + str(prices[i]) + '.00')

    return prices


def set_loc(lat, long):

    global se2lib

    se2lib.driver.execute_script(
        "navigator.geolocation.getCurrentPosition = function(cb){cb({ coords: {accuracy: 20,altitude: null,altitudeAccuracy: null,heading: null,latitude: " + lat + ",longitude: " + long + ",speed: null}}); }")
    se2lib.driver.execute_script(
        "window.navigator.geolocation.getCurrentPosition = function(cb){cb({ coords: {accuracy: 20,altitude: null,altitudeAccuracy: null,heading: null,latitude: " + lat + ",longitude: " + long + ",speed: null}}); }")

def add_wait():
    time.sleep(5)
    