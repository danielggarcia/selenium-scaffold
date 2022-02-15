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
from testrunner.base.page_object import PageObject


class POLanding(PageObject):
    def __init__(self, driver: WebDriver, url: str = None):
        super().__init__(driver, url)
        self.sectionLinks = driver.find_elements(By.XPATH, '//ul/li/a')

    def go_to_section(self, link: str):
        results = list(filter(lambda item: item.get_attribute("text") == link or item.get_attribute("href").endswith(link), self.sectionLinks))
        if len(results) > 0:
            self.driver.get(results[0].get_attribute('href'))
