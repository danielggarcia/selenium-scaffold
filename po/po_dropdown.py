# Copyright [2021] [Daniel Garcia <contacto {at} danigarcia.org>]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from testrunner.base.page_object import PageObject


class PODropDown(PageObject):
    def __init__(self, driver: WebDriver, url: str = None):
        super().__init__(driver, url)
        self.dropdown = Select(driver.find_element(By.ID, 'dropdown'))

    def select_by_value(self, value: str):
        self.dropdown.select_by_value(value)

    def select_by_index(self, index: int):
        self.dropdown.select_by_index(index)

    def select_by_visible_text(self, text: str):
        self.dropdown.select_by_visible_text(text)

    def get_text(self):
        return self.dropdown.all_selected_options[0].text
