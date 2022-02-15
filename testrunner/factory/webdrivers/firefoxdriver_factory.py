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
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class FirefoxDriverFactory(WebDriverFactoryInterface):
    """
    Internal class that generates a FirefoxDriver instance
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
            if self.driver_configuration['driver']['type'] != "FirefoxDriver":
                raise Exception(__class__.__name__ + ": The provided configuration is not compatible with FirefoxDriver")

        except Exception as e:
            logger.exception("Error loading firefox default configuration")
            raise e


    def _create_webdriver_options_(self):
        try:
            firefox_options = webdriver.FirefoxOptions()
            firefox_profile = webdriver.FirefoxProfile()
            firefox_capabilities = DesiredCapabilities.FIREFOX

            # Get Geckodriver path
            if not os.path.isfile(self.driver_configuration['driver']['executable_path']):
                firefox_options.driver_executable_path = GeckoDriverManager().install()
            else:
                firefox_options.driver_executable_path = self.driver_configuration['driver']['executable_path']

            # Browser binary, if provided
            options = self.driver_configuration['options']
            if os.path.isfile(options['binary_path']):
                firefox_options.binary_location = options['binary_path']

            # Allow self-signed certificates
            if 'accept_untrusted_certs' in options:
                firefox_profile.accept_untrusted_certs = options['accept_untrusted_certs']

            # Preferences
            if 'preferences' in options is not None:
                for key in options['preferences']:
                    if options['preferences'][key] == "":
                        firefox_profile.set_preference(key, "")
                    else:
                        firefox_profile.set_preference(key, options['preferences'][key])

            if 'extensions' in options is not None:
                for key in options['extensions']:
                    firefox_profile.add_extension(key)

            firefox_capabilities['marionette'] = True

            return (firefox_options, firefox_profile, firefox_capabilities)

        except Exception as e:
            logger.exception("Error creating Firefox options")
            raise e


    def create_instance(self):
        """
        Creates a FirefoxDriver instance by loading configuration parameters provided in constructor
        :return: A configured FirefoxDriver instance
        """
        firefox_configuration = self._create_webdriver_options_()
        firefox_options = firefox_configuration[0]
        firefox_profile = firefox_configuration[1]
        firefox_capabilities = firefox_configuration[2]

        try:
            driver = webdriver.Firefox(executable_path=firefox_options.driver_executable_path,
                                       firefox_profile=firefox_profile,
                                       desired_capabilities=firefox_capabilities)
            return driver

        except WebDriverException as e:
            logger.exception(__class__.__name__ + ": Error initializing ChromeWebDriver")
            raise e
