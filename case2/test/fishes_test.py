import os
import unittest
from selenium import webdriver
from .environment import load_e2e_config
from .page_object import FishesList


DRIVERS_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', 'drivers')
E2E_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'e2e.config.yml')


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
        driver_path = os.path.join(DRIVERS_DIR_PATH, 'chromedriver')
        options = webdriver.chrome.options.Options()
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
