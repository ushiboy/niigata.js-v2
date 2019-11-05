import os
import unittest
from selenium import webdriver
from .environment import load_e2e_config
from .page_object import FishList


DRIVERS_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', 'drivers')
E2E_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'e2e.config.yml')


class FishListTest(unittest.TestCase):

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

    def test_the_list_is_loaded_dynamically(self):
        """
        一覧が動的に読み込まれること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        assert len(rows) == 3
        r1, r2, r3 = rows;
        assert r1.get_name() == 'まぐろ'
        assert r2.get_name() == 'はまち'
        assert r3.get_name() == 'かつお'

    def test_an_alert_will_appear_when_OK_click_without_selecting_an_item(self):
        """
        未選択状態で"けってい"するとアラートがでること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        alert = p.click_select()
        assert alert.text == "せんたくしてください"
        alert.accept()

    def test_the_selection_result_is_displayed_when_selecting_an_item_in_the_list_and_OK_click(self):
        """
        一覧のアイテムを1件選択して"けってい"すると選択結果が表示されること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        rows[0].click_checkbox()

        alert = p.click_select()
        assert alert.text == "まぐろ"
        alert.accept()

    def test_the_selection_result_is_displayed_when_selecting_some_items_in_the_list_and_OK_click(self):
        """
        一覧のアイテムを複数件選択して"けってい"すると選択結果が表示されること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        rows[0].click_checkbox()
        rows[1].click_checkbox()

        alert = p.click_select()
        assert alert.text == "まぐろ,はまち"
        alert.accept()

    def test_all_items_will_be_selected_when_the_overall_check_click(self):
        """
        全体チェックをするとすべてのアイテムが選択されること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        rows[0].click_checkbox()

        alert1 = p.click_select()
        assert alert1.text == "まぐろ"
        alert1.accept()

        p.click_all_check()

        alert2 = p.click_select()
        assert alert2.text == "まぐろ,はまち,かつお"
        alert2.accept()

    def test_deselect_all_items_when_click_uncheck_all(self):
        """
        全部チェックを外すとすべてのアイテムが選択解除になること
        """
        p = FishList(self.driver, self.target_origin)\
                .open()\
                .wait_for_row_to_finish_loading()

        rows = p.get_rows()
        rows[0].click_checkbox()
        rows[1].click_checkbox()
        rows[2].click_checkbox()

        alert1 = p.click_select()
        assert alert1.text == "まぐろ,はまち,かつお"
        alert1.accept()

        p.click_all_check()

        alert2 = p.click_select()
        assert alert2.text == "せんたくしてください"
        alert2.accept()


if __name__ == '__main__':
    unittest.main()
