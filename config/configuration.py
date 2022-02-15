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

config_dir = "config"
config_file = "config.yaml"
dev_config_file = "config_dev.yaml"
prod_config_file = "config_prod.yaml"

path = os.path.join(config_dir, config_file)

def read_yaml(cfg_path):
    with open(cfg_path, 'rt') as fd:
        try:
            dictionary = yaml.safe_load(fd.read())
            return dictionary
        except Exception as e:
            print("Unable to load configuration file", path)
            raise e


env = read_yaml(path)
additional_config_path = os.path.join(config_dir, dev_config_file) if env['environment'] == 'dev' else os.path.join(
    config_dir, prod_config_file)
additional_config = read_yaml(additional_config_path)

for key in additional_config:
    env[key] = additional_config[key]
