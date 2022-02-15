# Copyright [2021] [Daniel Garcia <contacto {at} danigarcia.org]
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

import os
import logging
import logging.config
import yaml
from config.configuration import env

__log_cfg_path = env.get("log_config_path")
__default_level = env.get("log_default_level")
__env = env.get('environment')


def get_basic_logger(default_level=logging.INFO):
    logging.basicConfig(default_level)
    logger = logging.getLogger(__name__)
    return logger


def get_logger(path=__log_cfg_path, default_level=__default_level):
    if os.path.exists(path):
        with open(path, 'rt') as fd:
            try:
                yaml_config = yaml.safe_load(fd.read())
                logging.config.dictConfig(yaml_config)
                logger = logging.getLogger(__env)
                logger.setLevel(__default_level)
                return logger
            except Exception as e:
                logger = get_basic_logger(default_level)
                logger.exception("Error loading logger configuration")
                return logger
    else:
        return get_basic_logger()

logger = get_logger()
