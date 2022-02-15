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
import sys

from testrunner.util.log_setup import logger
from config.configuration import env
from selenium.webdriver.remote.webdriver import WebDriver

from testrunner.util.utils import Utils


class WebDriverFactory:
    __browserProperties__ = None
    __driver__ = None

    @staticmethod
    def __load_configuration__(config_file_path: str):
        if os.path.exists(config_file_path):
            with open(config_file_path, 'rt') as fd:
                try:
                    driver_config = yaml.safe_load(fd.read())
                    return driver_config
                except Exception as e:
                    logger.exception("Error loading driver configuration from file '{}'".format(config_file_path))
        else:
            raise Exception("Driver configuration file '{}' not found.".format(config_file_path))


    @staticmethod
    def __create_factory__(driver_configuration: dict):
        try:
            # Extract driver.type field from YAML, and compose the factory name from it using reflection
            # Additional webdriver support can be added just creating additional factories, whose names
            # must match with the format {driver.type}Factory pattern
            factory_name = driver_configuration['driver']['type']

            # Import WebDriver factory dynamically
            webdriver_factory_package = sys.modules[__name__].__package__ + ".webdrivers"
            current_factory_module = webdriver_factory_package + ".{}_factory".format(factory_name.lower())
            current_factory_classname = "{}Factory".format(factory_name)
            factory_class = Utils.dynamic_import(current_factory_module, current_factory_classname)
            factory = factory_class(driver_configuration)

            return factory
        except Exception as e:
            logger.exception(__class__.__name__ + ":")


    @staticmethod
    def __search_webdriver_configuration_by_name__(browser_name: str = None, exact_match: bool = False):
        try:
            config_file_path = ""

            if browser_name is None or browser_name == "":
                return config_file_path

            file_tree = sorted(os.listdir(env.get("webdriver_config_dir")))
            for file_i in file_tree:
                if exact_match and file_i.lower().replace(".yaml") == browser_name.lower().replace(".yaml"):
                        config_file_path = os.path.join(env.get("webdriver_config_dir", file_i))
                        break
                elif browser_name.lower() in file_i.lower():
                        config_file_path = os.path.join(env.get("webdriver_config_dir"), file_i)
                        break
            return config_file_path
        except Exception as e:
            logger.exception(__class__.__name__ + ": error while searching for configuration '{}'".format(browser_name))


    @staticmethod
    def __apply_extended_options__(driver: WebDriver, options: dict):
        if "window_position" in options and type(options["window_position"]) is list and len(options["window_position"]) == 2:
            driver.set_window_position(options["window_position"][0], options["window_position"][1])
        if "window_size" in options and type(options["window_size"]) is list and len(options["window_size"]) == 2:
            driver.set_window_size(options["window_size"][0], options["window_size"][1])
        if "start_maximized" in options and options['start_maximized']:
            driver.maximize_window()
        elif "start_minimized" in options and options['start_minimized']:
            driver.minimize_window()
        if "implicit_timeout" in options:
            driver.implicitly_wait(int(options["implicit_timeout"]))
            driver.capabilities['timeouts']['implicit'] = int(options["implicit_timeout"])
        if "page_load_timeout" in options:
            driver.set_page_load_timeout(int(options["page_load_timeout"]))
            driver.capabilities['timeouts']['page_load'] = int(options["page_load_timeout"])


    @staticmethod
    def create_instance(browser_name: str = None, config_file_path: str = None, exact_match: bool = False):
        """
        Creates a WebDriver instance by providing a YAML configuration path with configuration parameters
        :param browser_name: name of the browser to drive. This parameter will search in config/webdrivers folder for
        the first configuration file matching this parameter.
        :param config_file_path: path to YAML configuration file. If not provided, a default instance will be spawned
        loading configuration from config/webdrivers/default.yaml file
        :param exact_match: if browser_name is provided, search for the whole configuration file or just for part of it
        :return: WebDriver instance
        """
        try:
            config_file_path_by_name = ""
            if browser_name is not None:
                config_file_path_by_name = WebDriverFactory.__search_webdriver_configuration_by_name__(browser_name,
                                                                                                       exact_match)
            # If no config_file_path or browser_name are provided, get the default configuration file
            if (config_file_path is None or not os.path.isfile(config_file_path)) and config_file_path_by_name == "":
                config_file_path = env.get("default_webdriver_config_file")
            # If config file is provided, it will prevail over browser_name
            elif config_file_path is not None and os.path.isfile(config_file_path):
                pass
            # Otherwise, config file will be the first match in the configuration folder
            else:
                config_file_path = config_file_path_by_name

            # Generate dictionary from YAML, and create an instance of driver factory
            driver_config = WebDriverFactory.__load_configuration__(config_file_path)
            driver_factory = WebDriverFactory.__create_factory__(driver_config)

            # Use factory to create a WebDriver instance
            driver = driver_factory.create_instance()
            if "extended_options" in driver_config:
                WebDriverFactory.__apply_extended_options__(driver, driver_config["extended_options"])

            return driver
        except Exception as e:
            logger.exception(__class__.__name__ + ": error creating instance")
            raise e
