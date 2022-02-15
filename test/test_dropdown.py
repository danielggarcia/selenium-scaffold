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
import pytest

from po.po_dropdown import PODropDown
from po.po_landing import POLanding
from testrunner.factory.webdriver_factory import WebDriverFactory


@pytest.fixture
def driver():
    driver = WebDriverFactory.create_instance("chrome")
    return driver


def test_dropdown(driver):
    landing = POLanding(driver, "https://the-internet.herokuapp.com/")
    landing.go_to_section("dropdown")

    dropdown = PODropDown(driver)
    dropdown.select_by_index(1)

    assert (dropdown.get_text() == "Option 1")
