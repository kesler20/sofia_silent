from selenium import webdriver as wb
import unittest
import os
import sys
import page
import element
import locator


os.chdir(r"C:\Users\CBE-User 05\Protocol\Sofia")

if __package__:
    from Web_driver.logs_webdriver.webdriver_logging import logger, logging
else:
    sys.path.append(os.path.join(os.getcwd(), 'Web_driver'))
    from logs_webdriver.webdriver_logging import logger, logging

print(
    '__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(
        __file__, __name__, str(__package__)
    )
)


class TestSearch(unittest.TestCase):

    def setUp(self):
        web_driver_path = os.path.join(os.getcwd(), 'Web_driver', 'msedgedriver.exe')
        self.driver = wb.Edge(web_driver_path)
        # get python documentation
        self.driver.get('http://www.python.org')

    def test_logging(self):
        print('The test log has ran succesfully')
        self.assertLogs(logger, logging.DEBUG)
        # self.assertFalse(1,1) red

    def test_search_in_python_org(self):
        """Tests python.org search feature. Searches for the word "pycon" then
        verified that some results show up.  Note that it does not look for
        any particular text in search results page. This test verifies that
        the results were not empty."""

        # Load the main page. In this case the home page of Python.org.
        main_page = page.MainPage(self.driver)
        # Checks if the word "Python" is in title
        self.assertTrue(main_page.is_title_matches(),
                        "python.org title doesn't match.")
        # Sets the text of search textbox to "pycon"
        main_page.search_text_element = "pycon"
        main_page.click_go_button()
        search_results_page = page.SearchResultsPage(self.driver)
        # Verifies that the results page is not empty
        self.assertTrue(search_results_page.is_results_found(),
                        "No results found.")

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
