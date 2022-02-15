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
import os.path
import yaml

from testrunner.util.log_setup import logger
from testrunner.factory.webdrivers.webdriverfactory_interface import WebDriverFactoryInterface
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class ChromeDriverFactory(WebDriverFactoryInterface):
    """
    Internal class that generates a ChromeDriver instance
    """

    def __init__(self, driver_configuration: dict = None, config_file_path: str = None):
        self.driver_configuration = driver_configuration
        self.config_file_path = config_file_path

        if config_file_path is not None and os.path.isfile(config_file_path):
            self._load_default_options_(config_file_path)


    def _load_default_options_(self, config_file_path: str = None):
        if config_file_path is None:
            cfg_path = os.path.join("config", "webdrivers", "default.yaml")
        else:
            cfg_path = config_file_path
        try:
            with open(cfg_path, 'rt') as fd:
                self.driver_configuration = yaml.safe_load(fd.read())
            if self.driver_configuration['driver']['type'] != "ChromeDriver":
                raise Exception(__class__.__name__ + ": The provided configuration is not compatible with ChromeDriver")

        except Exception as e:
            logger.exception("Error loading chrome default configuration")
            raise e


    def _create_webdriver_options_(self):
        try:
            chrome_options = webdriver.ChromeOptions()

            # Get chromedriver path
            if not os.path.isfile(self.driver_configuration['driver']['executable_path']):
                chrome_options.driver_executable_path = ChromeDriverManager().install()
            else:
                chrome_options.driver_executable_path = self.driver_configuration['driver']['executable_path']

            # Browser binary, if provided
            options = self.driver_configuration['options']
            if os.path.isfile(options['binary_path']):
                chrome_options.binary_location = options['binary_path']

            # Arguments
            if options['arguments'] is not None:
                for key in options['arguments']:
                    if options['arguments'][key] == "":
                        chrome_options.add_argument(key)
                    else:
                        chrome_options.add_argument(key + "=" + options['arguments'][key])

            # Experimental options
            if options['experimental_options'] is not None:
                for key in options['experimental_options']:
                    if options['experimental_options'][key] == "":
                        chrome_options.add_experimental_option(key, "")
                    else:
                        chrome_options.add_experimental_option(key, options['experimental_options'][key])

            return chrome_options

        except Exception as e:
            logger.exception("Error creating Chrome options")
            raise e


    def create_instance(self):
        """
        Creates a ChromeDriver instance by loading configuration parameters provided in constructor
        :return: A configured ChromeDriver instance
        """
        chrome_options = self._create_webdriver_options_()

        try:
            driver = webdriver.Chrome(executable_path=chrome_options.driver_executable_path,
                                      chrome_options=chrome_options,
                                      service_args=["--verbose"])

            return driver

        except WebDriverException as e:
            logger.exception(__class__.__name__ + ": Error initializing ChromeWebDriver")
            raise e
