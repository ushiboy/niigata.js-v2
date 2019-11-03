from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

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


