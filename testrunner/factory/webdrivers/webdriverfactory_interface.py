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
class WebDriverFactoryInterface:

    driver_configuration = {}
    config_file_path = ""

    def _load_default_options_(self, config_file_path: str = None):
        """
        Loads default options from config/webdrivers folder and stores it in driver_configuration attribute
        :param config_file_path: path to the YAML file with the configuration
        :return:
        """
        pass

    def _create_webdriver_options_(self):
        """
        Takes the values stored in the generic dictionary driver_configuration and generates a driver-specific
        configuration object.
        :return: webdriver-specific configuration object
        """
        pass

    def create_instance(self):
        """
        Creates a WebDriver instance by loading configuration parameters provided in constructor
        :return: A configured WebDriver instance
        """
        pass