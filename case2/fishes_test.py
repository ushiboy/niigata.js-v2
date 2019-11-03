import os
import unittest
import yaml

from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


DRIVERS_DIR_PATH = os.path.join(os.path.dirname(__file__), '.', 'drivers')
E2E_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.', 'e2e.config.yml')


def load_e2e_config(filepath):
    with open(filepath, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    config = dict()
    workers = data.get('workers', [])
    for i, w in enumerate(workers):
        w['id'] = i + 1
        config['gw%d' % i] = w
    return config


class FishesList(object):

    def __init__(self, driver, target_origin):
        self._driver = driver
        self._target_origin = target_origin

    def open(self):
        self._driver.get(self._target_origin)
        return self

    def wait_for_row_to_finish_loading(self):
        WebDriverWait(self._driver, 5).until(
            lambda d: len(self.get_rows()) != 0
        )
        return self

    def click_select(self):
        self._driver.find_element_by_id('select-button').click()
        return self._driver.switch_to.alert

    def click_all_check(self):
        self._driver.find_element_by_id('all-check').click()
        return self

    def get_rows(self):
        rows = self._driver.find_element_by_id('fishes-list')\
                .find_elements_by_tag_name('tr')
        return list(map(lambda el: FishesListRow(self._driver, el), rows))


class FishesListRow(object):

    def __init__(self, driver, el):
        self._driver = driver
        self._el = el

    def get_name(self):
        return self._el.find_elements_by_tag_name('td')[1].text

    def click_checkbox(self):
        self._el.find_element_by_class_name('select-row').click()
        return self


class FishesListTest(unittest.TestCase):

    def setUp(self):
        target_host = os.environ.get('SERVER_HOST', 'localhost')
        target_port = '8080'
        worker = os.environ.get('PYTEST_XDIST_WORKER')
        if worker is not None:
            config = load_e2e_config(E2E_CONFIG_PATH)
            c = config[worker]
            target_port = str(c['web_port'])

        self.target_origin = 'http://%s:%s/' % (target_host, target_port)
        use_headless = os.environ.get('HEADLESS', False)
        driver_path = os.path.join(DRIVERS_DIR_PATH, 'chromedriver')
        options = webdriver.chrome.options.Options()
        if use_headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

    def test_show_fishes_list_rows(self):
        p = FishesList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        assert len(rows) == 3
        r1, r2, r3 = rows;
        assert r1.get_name() == 'まぐろ'
        assert r2.get_name() == 'はまち'
        assert r3.get_name() == 'かつお'

    def test_click_select_button_when_no_select_items(self):
        p = FishesList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        alert = p.click_select()
        assert alert.text == "せんたくしてください"
        alert.dismiss()

    def test_click_select_button_when_one_select_item(self):
        p = FishesList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        rows[0].click_checkbox()
        alert = p.click_select()

        assert alert.text == "まぐろ"
        alert.dismiss()


if __name__ == '__main__':
    unittest.main()
